# ZSequencer Network Local Setup Guide

This guide explains how to set up and run a **ZSequencer Network** locally using the **EigenLayer CLI**.

In this guide, we will configure a network with **4 operators**.

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

Assume we want to start 4 operators with names `zsequencer-operator1` to `zsequencer-operator4`:

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

This generates key files in the specified directory.

---

### Step 4: Set Up `docker-compose.yml`

Run the following commands to create a working directory and fetch `docker-compose.yml` and also prepare files structure for nodes.:

#### Multiple Operators

For 4 operators, create separate folders and files for each operator:

1. Run the following commands:
   ```bash
   mkdir zsequencer-operator1 && touch ./zsequencer-operator1/apps.json && touch ./zsequencer-operator1/nodes.json && cd zsequencer-operator1 &&
   curl -o docker-compose.yml https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/docker-compose-pull.yml && curl -o .env https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/.env.example

   mkdir zsequencer-operator2 && touch ./zsequencer-operator2/apps.json && touch ./zsequencer-operator2/nodes.json && cd zsequencer-operator2 &&
   curl -o docker-compose.yml https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/docker-compose-pull.yml && curl -o .env https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/.env.example

   mkdir zsequencer-operator3 && touch ./zsequencer-operator3/apps.json && touch ./zsequencer-operator3/nodes.json && cd zsequencer-operator3 &&
   curl -o docker-compose.yml https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/docker-compose-pull.yml && curl -o .env https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/.env.example

   mkdir zsequencer-operator4 && touch ./zsequencer-operator4/apps.json && touch ./zsequencer-operator4/nodes.json && cd zsequencer-operator4 &&
   curl -o docker-compose.yml https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/docker-compose-pull.yml && curl -o .env https://raw.githubusercontent.com/zellular-xyz/zsequencer/main/.env.example
   ```

Example structure:

```
- zsequencer-operator1
  - docker-compose.yml
  - .env
  - apps.json
  - nodes.json
- zsequencer-operator2
  - docker-compose.yml
  - .env
  - apps.json
  - nodes.json
- zsequencer-operator3
  - docker-compose.yml
  - .env
  - apps.json
  - nodes.json
- zsequencer-operator4
  - docker-compose.yml
  - .env
  - apps.json
  - nodes.json
```

---

### Step 5: Add Configuration Files

Each operator folder requires two files:

1. `apps.json`
2. `nodes.json`

#### Example `apps.json`

```json
{
  "<name>": {
    "url": "",
    "public_keys": []
  }
}
```

#### Example `nodes.json`

Below are the `nodes.json` files for the 4 operators with specified ports (5101, 5102, 5103, 5104):

**Operator 1:**

```json
{
    "0xethAddress1": {
        "id": "0xethAddress1",
        "public_key_g2": "<public_key_g2_value1>",
        "address": "0xethAddress1",
        "socket": "http://127.0.0.1:5101",
        "stake": 10
    }
}
```

**Operator 2:**

```json
{
    "0xethAddress2": {
        "id": "0xethAddress2",
        "public_key_g2": "<public_key_g2_value2>",
        "address": "0xethAddress2",
        "socket": "http://127.0.0.1:5102",
        "stake": 10
    }
}
```

**Operator 3:**

```json
{
    "0xethAddress3": {
        "id": "0xethAddress3",
        "public_key_g2": "<public_key_g2_value3>",
        "address": "0xethAddress3",
        "socket": "http://127.0.0.1:5103",
        "stake": 10
    }
}
```

**Operator 4:**

```json
{
    "0xethAddress4": {
        "id": "0xethAddress4",
        "public_key_g2": "<public_key_g2_value4>",
        "address": "0xethAddress4",
        "socket": "http://127.0.0.1:5104",
        "stake": 10
    }
}
```

---


### Step 6: Fill the `.env` File

Update the `.env` file for each operator folder using the parameters below. Ensure `ZSEQUENCER_REGISTER_OPERATOR=false`.

#### Example `.env` Files for Each Operator

**Operator 1:**
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

**Operator 2:**
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

**Operator 3:**
```ini
ZSEQUENCER_BLS_KEY_FILE=~/.eigenlayer/operator_keys/zsequencer-operator3.bls.key.json
ZSEQUENCER_BLS_KEY_PASSWORD='password3'
ZSEQUENCER_ECDSA_KEY_FILE=~/.eigenlayer/operator_keys/zsequencer-operator3.ecdsa.key.json
ZSEQUENCER_ECDSA_KEY_PASSWORD='password3'
ZSEQUENCER_REGISTER_SOCKET=http://127.0.0.1:5103
ZSEQUENCER_NODES_FILE=./nodes.json
ZSEQUENCER_APPS_FILE=./apps.json
ZSEQUENCER_SNAPSHOT_PATH=./db
ZSEQUENCER_PORT=5103
ZSEQUENCER_INIT_SEQUENCER_ID=0xethAddress3
ZSEQUENCER_REGISTER_OPERATOR=false
```

**Operator 4:**
```ini
ZSEQUENCER_BLS_KEY_FILE=~/.eigenlayer/operator_keys/zsequencer-operator4.bls.key.json
ZSEQUENCER_BLS_KEY_PASSWORD='password4'
ZSEQUENCER_ECDSA_KEY_FILE=~/.eigenlayer/operator_keys/zsequencer-operator4.ecdsa.key.json
ZSEQUENCER_ECDSA_KEY_PASSWORD='password4'
ZSEQUENCER_REGISTER_SOCKET=http://127.0.0.1:5104
ZSEQUENCER_NODES_FILE=./nodes.json
ZSEQUENCER_APPS_FILE=./apps.json
ZSEQUENCER_SNAPSHOT_PATH=./db
ZSEQUENCER_PORT=5104
ZSEQUENCER_INIT_SEQUENCER_ID=0xethAddress4
ZSEQUENCER_REGISTER_OPERATOR=false
```

---

### Step 7: Run the Nodes

Start the ZSequencer nodes for each operator:

1. Navigate to each operator folder:
   ```bash
   cd zsequencer-operator1
   docker compose up -d
   ```
2. Repeat for all other operator folders:
   ```bash
   cd ../zsequencer-operator2
   docker compose up -d

   cd ../zsequencer-operator3
   docker compose up -d

   cd ../zsequencer-operator4
   docker compose up -d
   ```

Verify the nodes are running:

```bash
docker ps
```

---

### Troubleshooting

Check logs if issues occur:

```bash
docker compose logs
```


