import os
import sys
import json
from eigensdk.crypto.bls import attestation

# Check if node_ip and node_port are provided as command-line arguments
if len(sys.argv) != 3:
    raise ValueError("Please provide NODE_IP and NODE_PORT as command-line arguments.")

node_ip = sys.argv[1]
node_port = sys.argv[2]

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Variables from environment
sequencer_id = os.getenv("ZSEQUENCER_INIT_SEQUENCER_ID")
file_path = os.getenv("ZSEQUENCER_BLS_KEY_FILE")
password = os.getenv("ZSEQUENCER_BLS_KEY_PASSWORD")

if not sequencer_id or not file_path or not password:
    raise ValueError("Ensure ZSEQUENCER_INIT_SEQUENCER_ID, FILE_PATH, and PASSWORD are set in the environment variables")

# Generate public_key_g2
key_pair = attestation.KeyPair.read_from_file(file_path, password)
public_key_g2 = key_pair.pub_g2.getStr(10).decode("utf-8")

# Node configuration
node_socket = f"http://{node_ip}:{node_port}"
stake = 10

# Prepare data for nodes.json
nodes_data = {
    sequencer_id: {
        "id": sequencer_id,
        "public_key_g2": public_key_g2,
        "address": sequencer_id,
        "socket": node_socket,
        "stake": stake
    }
}

# Write to nodes.json
with open("nodes.json", "w") as nodes_file:
    json.dump(nodes_data, nodes_file, indent=4)

print(f"nodes.json file has been written successfully with node ID: {sequencer_id}")
