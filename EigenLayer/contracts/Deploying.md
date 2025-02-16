# **Cloning and Deploying EigenLayer Contracts with Forge & Foundry**

This guide walks you through cloning the **EigenLayer contracts**, setting up Foundry, preparing wallets, and deploying the contracts locally.

---

## **1. Prerequisites**
Ensure you have the following installed:
- **Foundry** (includes `forge`, `cast`, `anvil`)
- **Git**
- **Node.js & npm** (for dependencies)
- **jq** (for JSON processing, optional)

### **Installing Foundry**
```sh
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

### **Checking Installation**
```sh
forge --version
anvil --version
```

---

## **2. Clone the EigenLayer Contracts Repository**
```sh
git clone https://github.com/Layr-Labs/eigenlayer-contracts.git
cd eigenlayer-contracts
```

---

## **3. Install Dependencies**
```sh
forge install
forge build
```
This will compile the smart contracts.

---

## **4. Create Necessary Directories**
Some directories required for saving deployment details may not exist. Create them manually:
```sh
mkdir -p script/output/local
mkdir -p local
```
This ensures Foundry can store required output files.

---

## **5. Start a Local Ethereum Node (Anvil)**
We will use **Anvil** (Foundry’s local Ethereum testnet):
```sh
anvil
```
Anvil will start a local node on **http://127.0.0.1:8545** and print **test wallets** with private keys.

---

## **6. Prepare Wallets**
Foundry provides **pre-funded** wallets when running `anvil`. You can use one of them for deployment.

If you need a new wallet, generate one using:
```sh
cast wallet new
```
This will output:
```sh
Private Key: 0x...
Address: 0x...
```
Save this **private key** for deployment.

If using Anvil’s default key:
```
0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

---

## **7. Deploy EigenLayer Contracts**
Run the following command to deploy from scratch:
```sh
forge script script/deploy/local/Deploy_From_Scratch.s.sol \
    --fork-url http://127.0.0.1:8545 \
    --broadcast \
    --skip-simulation \
    --sig "run(string memory)" "local/deploy_from_scratch.anvil.config.json" \
    --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

### **Explanation of Flags**
- `--fork-url http://127.0.0.1:8545` → Uses Anvil as the local Ethereum node
- `--broadcast` → Broadcasts the transactions on-chain
- `--skip-simulation` → Skips the dry-run simulation
- `--sig "run(string memory)"` → Calls the `run()` function of the deploy script
- `--private-key` → Specifies the deployer wallet

---

## **8. Deploy Slashing Contracts**
To deploy **slashing contracts**, run:
```sh
forge script script/deploy/local/deploy_from_scratch.slashing.s.sol \
    --fork-url http://127.0.0.1:8545 \
    --broadcast \
    --skip-simulation \
    --sig "run(string memory)" "local/deploy_from_scratch.slashing.anvil.config.json" \
    --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

---

## **9. Verify Deployment**
After deployment, verify the contract addresses:
```sh
cast call <contract_address> "<function_signature>"
```

Example:
```sh
cast call 0x1234567890abcdef1234567890abcdef12345678 "owner()(address)"
```

To check deployed contract logs:
```sh
cat out/deployments.json | jq .
```

---

## **10. (Optional) Deploy on a Testnet**
For testnet deployment, replace the fork URL with an **Alchemy** or **Infura** RPC:
```sh
forge script script/deploy/local/Deploy_From_Scratch.s.sol \
    --fork-url https://eth-goerli.alchemyapi.io/v2/YOUR_API_KEY \
    --broadcast \
    --skip-simulation \
    --sig "run(string memory)" "local/deploy_from_scratch.anvil.config.json" \
    --private-key YOUR_PRIVATE_KEY
```

---

## **11. Debugging Tips**
- If deployment fails, check errors using:
  ```sh
  forge test -vvvv
  ```
- To clean and rebuild:
  ```sh
  forge clean
  forge build
  ```
- To check gas usage:
  ```sh
  forge snapshot
  ```

