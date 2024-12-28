
# Local Setup Guide for ZSequencer Network

This guide details the steps to set up and run a **ZSequencer Network** locally using the **EigenLayer CLI**. We will configure a network with **4 operators**.

---

## Step 1: Install Docker

Install Docker following the official guide:

- [Docker Installation Guide](https://docs.docker.com/engine/install/#server)

Verify your installation:

```bash
docker --version
```

---

## Step 2: Install EigenLayer CLI

Install the EigenLayer CLI using the official operator guide:

- [EigenLayer CLI Installation](https://docs.eigenlayer.xyz/eigenlayer/operator-guides/operator-installation#install-cli-using-binary)

Confirm the installation:

```bash
eigenlayer --version
```

---

## Step 3: Generate Keys

You need to generate **ECDSA** and **BLS** keys for each operator, which will be stored in the directory:

```
~/.eigenlayer/operator_keys
```

### Commands to Generate Keys:

```bash
eigenlayer operator keys create --key-type ecdsa <operator_name>
eigenlayer operator keys create --key-type bls <operator_name>
```

### Example for 4 Operators:

```bash
eigenlayer operator keys create --key-type ecdsa zsequencer-operator1
eigenlayer operator keys create --key-type bls zsequencer-operator1

eigenlayer operator keys create --key-type ecdsa zsequencer-operator2
eigenlayer operator keys create --key-type bls zsequencer-operator2

eigenlayer operator keys create --key-type ecdsa zsequencer-operator3
eigenlayer operator keys create --key-type bls zsequencer-operator3

eigenlayer operator keys create --key-type ecdsa zsequencer-operator4
eigenlayer operator keys create --key-type bls zsequencer-operator4
```

---

## Step 4: Set Up `docker-compose.yml`

### Create Operator Directories and Files

Run the following commands to set up directories for each operator:

```bash
for i in {1..4}
do
  mkdir zsequencer-operator$i
  touch ./zsequencer-operator$i/apps.json ./zsequencer-operator$i/nodes.json
  cd zsequencer-operator$i
  curl -o docker-compose.yml https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/docker-compose-local-pull.yml
  curl -o .env https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/.env.example
  cd ..
done
```

The directory structure should look like this:

```
zsequencer-operator1/
  - docker-compose.yml
  - .env
  - apps.json
  - nodes.json
zsequencer-operator2/
  - docker-compose.yml
  - .env
  - apps.json
  - nodes.json
zsequencer-operator3/
  - docker-compose.yml
  - .env
  - apps.json
  - nodes.json
zsequencer-operator4/
  - docker-compose.yml
  - .env
  - apps.json
  - nodes.json
```

---

## Step 5: Configure `apps.json`

Each operator needs a `apps.json` file. Use the following template:

```json
{
  "<name>": {
    "url": "",
    "public_keys": []
  }
}
```

Replace `<name>` with "ZSequencer".

---

## Step 6: Configure `.env` Files

Each operator requires a unique `.env` file. Follow the structure below, adjusting the values for each operator's specific configuration.  

### Example `.env` File for Operator 1:

```ini
ZSEQUENCER_BLS_KEY_FILE=~/.eigenlayer/operator_keys/zsequencer-operator1.bls.key.json
ZSEQUENCER_BLS_KEY_PASSWORD='password1'
ZSEQUENCER_ECDSA_KEY_FILE=~/.eigenlayer/operator_keys/zsequencer-operator1.ecdsa.key.json
ZSEQUENCER_ECDSA_KEY_PASSWORD='password1'
ZSEQUENCER_REGISTER_SOCKET=http://127.0.0.1:5101
ZSEQUENCER_NODES_FILE=./nodes.json
ZSEQUENCER_APPS_FILE=./apps.json
ZSEQUENCER_SNAPSHOT_PATH=./db
ZSEQUENCER_PORT=5101
ZSEQUENCER_INIT_SEQUENCER_ID=0xethAddress1
ZSEQUENCER_REGISTER_OPERATOR=false
```

### Customizing for Each Operator:

Repeat the process for operators 2, 3, and 4 by modifying the following:

1. **File Paths**: Update `ZSEQUENCER_BLS_KEY_FILE` and `ZSEQUENCER_ECDSA_KEY_FILE` with the corresponding operator key files (e.g., `zsequencer-operator2` for Operator 2).
2. **Passwords**: Set unique passwords for each operator (e.g., `password2`, `password3`, etc.).
3. **Ports**: Assign unique ports for each operator:
   - Operator 1: `5101`
   - Operator 2: `5102`
   - Operator 3: `5103`
   - Operator 4: `5104`
4. **Sequencer ID**: Replace `ZSEQUENCER_INIT_SEQUENCER_ID` with the correct Ethereum address for each operator.

### Example for Operator 2:

```ini
ZSEQUENCER_BLS_KEY_FILE=~/.eigenlayer/operator_keys/zsequencer-operator2.bls.key.json
ZSEQUENCER_BLS_KEY_PASSWORD='password2'
ZSEQUENCER_ECDSA_KEY_FILE=~/.eigenlayer/operator_keys/zsequencer-operator2.ecdsa.key.json
ZSEQUENCER_ECDSA_KEY_PASSWORD='password2'
ZSEQUENCER_REGISTER_SOCKET=http://127.0.0.1:5102
ZSEQUENCER_NODES_FILE=./nodes.json
ZSEQUENCER_APPS_FILE=./apps.json
ZSEQUENCER_SNAPSHOT_PATH=./db
ZSEQUENCER_PORT=5102
ZSEQUENCER_INIT_SEQUENCER_ID=0xethAddress2
ZSEQUENCER_REGISTER_OPERATOR=false
```

Repeat similarly for operators 3 and 4, ensuring the configurations are adjusted appropriately for their specific settings.
---

## Step 7: Build and Run Nodes

1. Build each operator's Docker image:
   ```bash
   for i in {1..4}
   do
     cd zsequencer-operator$i
     docker build --build-arg NODE_IP=127.0.0.1 --build-arg NODE_PORT=510$i --build-arg NODES_COUNT=4 -t zsequencer-operator$i .
     docker run -d --name zsequencer-operator$i zsequencer-operator$i
     docker exec zsequencer-operator$i cat /apps/nodes.json > nodes.json
     docker stop zsequencer-operator$i
     cd ..
   done
   ```

2. Update each `nodes.json` file with all operators' details. Ensure it contains entries for all public keys.

Example:

```json
{
  "0xethAddress1": {
    "id": "0xethAddress1",
    "public_key_g2": "<public_key_g2_value1>",
    "socket": "http://127.0.0.1:5101",
    "stake": 10
  },
  "0xethAddress2": {
    "id": "0xethAddress2",
    "public_key_g2": "<public_key_g2_value2>",
    "socket": "http://127.0.0.1:5102",
    "stake": 10
  },
  "0xethAddress3": {
    "id": "0xethAddress3",
    "public_key_g2": "<public_key_g2_value3>",
    "socket": "http://127.0.0.1:5103",
    "stake": 10
  },
  "0xethAddress4": {
    "id": "0xethAddress4",
    "public_key_g2": "<public_key_g2_value4>",
    "socket": "http://127.0.0.1:5104",
    "stake": 10
  }
}
```

3. Start the containers:

   ```bash
   for i in {1..4}
   do
     cd zsequencer-operator$i
     docker run --name zsequencer-operator$i
     cd ..
   done
   ```

---

## Step 8: Verify Setup

Check running containers:

```bash
docker ps -a
```

Check logs for troubleshooting:

```bash
docker compose logs
```

--- 
