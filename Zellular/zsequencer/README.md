# ZSequencer Local Setup Guide

## Part 1: Running EigenLayer Node

This guide explains how to set up and run a ZSequencer node locally using the EigenLayer.

### Recommended Node Specifications
To run a Zellular Sequencer node efficiently, the following hardware specifications are recommended:
- **General Purpose - large**
- 2 vCPUs
- 8 GB RAM
- 5 Mbps network bandwidth

---

### Step 1: Install Docker
Install Docker by following the official instructions:

- [Docker Installation Guide](https://docs.docker.com/engine/install/#server)

Verify the installation:
```bash
docker --version
```

---

### Step 2: Install EigenLayer CLI
Install the EigenLayer CLI using the official EigenLayer Operator Guide:

- [EigenLayer CLI Installation](https://docs.eigenlayer.xyz/eigenlayer/operator-guides/operator-installation#install-cli-using-binary)

Verify the installation:
```bash
eigenlayer --version
```

---

### Step 3: Generate Keys
Two types of keys are required: **ECDSA** and **BLS**. Generate these keys for each operator with a unique name.

The keys will be saved in:
```
~/.eigenlayer/operator_keys
```

#### Generate Keys
Run the following commands:
```bash
eigenlayer operator keys create --key-type ecdsa <operator_name>
eigenlayer operator keys create --key-type bls <operator_name>
```

#### Example
For an operator named `zellular`:
```bash
eigenlayer operator keys create --key-type ecdsa zellular
eigenlayer operator keys create --key-type bls zellular
```
This generates key files in the specified directory.

---

### Step 4: Set Up docker-compose.yml

Run the following commands to create a working directory and fetch `docker-compose.yml`:
```bash
mkdir zsequencer
cd zsequencer
curl -o docker-compose.yml https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/docker-compose-pull.yml
```

#### Setup Environment
Fetch the environment file template and save it as `.env`:
```bash
curl -o .env https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/.env.example
```

#### Multiple Operators
If you need multiple operators:
1. Create separate folders for each operator:
   ```bash
   mkdir zsequencer-operator1
   mkdir zsequencer-operator2
   mkdir zsequencer-operator3
   ```
2. Download `docker-compose.yml` and `.env` in each folder.
3. Update the `.env` files with unique parameters for each operator.

Example structure for multiple operators:
```
- zsequencer-operator1
  - docker-compose.yml
  - .env
- zsequencer-operator2
  - docker-compose.yml
  - .env
- zsequencer-operator3
  - docker-compose.yml
  - .env
```

---

### Step 5: Add Configuration Files
Each operator folder requires two files:
1. `apps.json`
2. `nodes.json`

#### Example `apps.json`
```json
{
  "<Name>": {
    "url": "",
    "public_keys": []
  }
}
```

#### Example `nodes.json`
```json
{
    "<ETH_ADDRESS>": {
        "id": "<ETH_ADDRESS>",
        "public_key_g2": "<public_key_g2_value>",
        "address": "<ETH_ADDRESS>",
        "socket": "http://127.0.0.1:[PORT]",
        "stake": 10
    }
}
```
- Replace `<ETH_ADDRESS>` with the ECDSA-generated ETH address.
- Replace `<public_key_g2_value>` with the BLS key.
- Update the `socket` with the correct IP and port.

#### Download Sample Files
```bash
curl -o apps.json https://raw.githubusercontent.com/ihedbit/zsequencer/main/samples/apps.json
curl -o nodes.json https://raw.githubusercontent.com/ihedbit/zsequencer/main/samples/nodes.json
```
Customize these files as needed for each operator.

---

### Step 6: Modify docker-compose.yml
Ensure the `docker-compose.yml` file has the following configuration:

```yaml
services:
  zsequencer:
    container_name: zsequencer-node
    image: zellular/zsequencer:latest
    network_mode: host
    ports:
      - "${ZSEQUENCER_PORT}:${ZSEQUENCER_PORT}"
    volumes:
      - "${ZSEQUENCER_BLS_KEY_FILE}:/app/bls_key.json"
      - "${ZSEQUENCER_ECDSA_KEY_FILE}:/app/ecdsa_key.json"
      - "${ZSEQUENCER_SNAPSHOT_PATH}:/db"
      - "${ZSEQUENCER_APPS_FILE}:/app/app.json"
      - "${ZSEQUENCER_NODES_FILE}:/app/nodes.json"
    environment:
      - ZSEQUENCER_BLS_KEY_FILE=/app/bls_key.json
      - ZSEQUENCER_ECDSA_KEY_FILE=/app/ecdsa_key.json
      - ZSEQUENCER_SNAPSHOT_PATH=/db
      - ZSEQUENCER_APPS_FILE=/app/app.json
      - ZSEQUENCER_NODES_FILE=/app/nodes.json
    env_file:
      - .env
```
Verify paths and ports are correct for your environment.

---

### Step 7: Fill the `.env` File
Update the `.env` file with the following parameters. Ensure `ZSEQUENCER_REGISTER_OPERATOR=false`:

```ini
# BLS and ECDSA key paths and passwords
ZSEQUENCER_BLS_KEY_FILE=~/.eigenlayer/operator_keys/<Operator_Name>.bls.key.json
ZSEQUENCER_BLS_KEY_PASSWORD='PASSWORD YOU ENTERED DURING KEY GENERATION.'
ZSEQUENCER_ECDSA_KEY_FILE=~/.eigenlayer/operator_keys/<Operator_Name>.ecdsa.key.json
ZSEQUENCER_ECDSA_KEY_PASSWORD='PASSWORD YOU ENTERED DURING KEY GENERATION.'

# Socket URL and node configuration paths
ZSEQUENCER_REGISTER_SOCKET=http://127.0.0.1:[PORT]
ZSEQUENCER_NODES_FILE=[OperatorFolderPath]/nodes.json
ZSEQUENCER_APPS_FILE=[OperatorFolderPath]/apps.json

# Archive and runtime configurations
ZSEQUENCER_SNAPSHOT_PATH=./db
ZSEQUENCER_PORT=[PORT]
ZSEQUENCER_INIT_SEQUENCER_ID=<ETH_ADDRESS>
ZSEQUENCER_REGISTER_OPERATOR=false
```

---

### Step 8: Run the Node
Start the ZSequencer node:
```bash
docker compose up -d
```
Verify the node is running:
```bash
docker ps
```

---

### Troubleshooting
Check logs if issues occur:
```bash
docker compose logs
```

