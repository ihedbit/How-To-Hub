# Bitcoin Core Setup Guide (Ubuntu)

## Overview
This guide provides instructions to install, configure, and run Bitcoin Core (`bitcoind`) on an Ubuntu system.

## Prerequisites
- Ubuntu 20.04 or later
- At least 350GB of free disk space (for full node sync)
- A stable internet connection

## Installation

### 1. Add Bitcoin PPA Repository
Bitcoin Core is available through a PPA repository. Run the following commands:

```bash
sudo add-apt-repository ppa:bitcoin/bitcoin
sudo apt update
```

### 2. Install Bitcoin Core

```bash
sudo apt install bitcoind bitcoin-cli
```

## Configuration

### 3. Create a Configuration File
Before starting `bitcoind`, create a configuration file:

```bash
mkdir -p ~/.bitcoin
nano ~/.bitcoin/bitcoin.conf
```

Add the following lines:
```ini
server=1
daemon=1
txindex=1
rpcuser=your_rpc_username
rpcpassword=your_rpc_password
rpcallowip=127.0.0.1
rpcport=8332
listen=1
```
Save and exit (`CTRL+X`, then `Y`, then `Enter`).

## Running Bitcoin Core

### 4. Start Bitcoin Daemon
Run the following command to start `bitcoind` in the background:

```bash
bitcoind -daemon
```

### 5. Check Node Status
Verify that `bitcoind` is running:

```bash
bitcoin-cli getblockchaininfo
```

### 6. View Logs
If you encounter issues, check logs:

```bash
tail -f ~/.bitcoin/debug.log
```

### 7. Stop Bitcoin Core
To safely stop the daemon, run:

```bash
bitcoin-cli stop
```

## Additional Options

### Running on Testnet
To run Bitcoin Core on testnet, add this line to `bitcoin.conf`:

```ini
testnet=1
```
Restart `bitcoind` for changes to take effect.

### Running on Regtest (Local Testing)
For private blockchain testing:

```ini
regtest=1
```

Start the node and generate test blocks:

```bash
bitcoind -daemon -regtest
bitcoin-cli -regtest generate 101
```

## Uninstalling Bitcoin Core
If you need to remove Bitcoin Core:

```bash
sudo apt remove bitcoind bitcoin-cli
rm -rf ~/.bitcoin
```

## Conclusion
Your Bitcoin node is now up and running! 🎉 You can use `bitcoin-cli` to interact with the node. For more information, visit the [Bitcoin Core documentation](https://bitcoincore.org/).

