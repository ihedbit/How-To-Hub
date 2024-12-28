import os
import sys
import json
from eigensdk.crypto.bls import attestation

# Check if node_ip, node_port, and nodes_count are provided as command-line arguments
if len(sys.argv) != 4:
    raise ValueError("Please provide NODE_IP, NODE_PORT, and NODES_COUNT as command-line arguments.")

node_ip = sys.argv[1]
node_port = int(sys.argv[2])  # Convert to integer
nodes_count = int(sys.argv[3])  # Convert to integer

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Variables from environment
sequencer_id = os.getenv("ZSEQUENCER_INIT_SEQUENCER_ID")
file_path = os.getenv("ZSEQUENCER_BLS_KEY_FILE")
password = os.getenv("ZSEQUENCER_BLS_KEY_PASSWORD")

if not sequencer_id or not file_path or not password:
    raise ValueError("Ensure ZSEQUENCER_INIT_SEQUENCER_ID, FILE_PATH, and PASSWORD are set in the environment variables")

# Generate public_key_g2 for the actual node
key_pair = attestation.KeyPair.read_from_file(file_path, password)
public_key_g2 = key_pair.pub_g2.getStr(10).decode("utf-8")

# Node configuration for the actual node
node_socket = f"http://{node_ip}:{node_port}"
stake = 10

# Prepare data for nodes.json
nodes_data = {}

for i in range(1, nodes_count + 1):
    eth_address = f"0xethAddress{i}"
    if i == 1:
        # Populate the first node with actual data
        nodes_data[eth_address] = {
            "id": sequencer_id,
            "public_key_g2": public_key_g2,
            "socket": node_socket,
            "stake": stake
        }
    else:
        # Populate the rest with placeholder data
        nodes_data[eth_address] = {
            "id": eth_address,
            "public_key_g2": f"<public_key_g2_value{i}>",
            "socket": f"http://{node_ip}:{node_port + i - 1}",
            "stake": stake
        }

# Write to nodes.json
with open("nodes.json", "w") as nodes_file:
    json.dump(nodes_data, nodes_file, indent=4)

print(f"nodes.json file has been written successfully with {nodes_count} nodes.")
