import socket
import random
from viterbi_encoder import viterbi_encode

import argparse

parser = argparse.ArgumentParser(description="Viterbi Encoder with Optional Bit Errors")
parser.add_argument("--error-rate", type=float, default=0.0, help="Bit error rate (e.g., 0.02 for 2%)")

args = parser.parse_args()

# === 1. Generate a 32x32 binary array using pure Python ===
data_array = [[random.randint(0, 1) for _ in range(32)] for _ in range(32)]

# === (Optional) Save to text file for verification ===
with open("original_binary_array.txt", "w") as f:
    for row in data_array:
        f.write(' '.join(str(bit) for bit in row) + '\n')

# === 2. Flatten to a bitstream (1 bit per pixel since it's binary) ===
data_bits = [bit for row in data_array for bit in row]  # list of 1024 bits


# === 3. Encode with Viterbi ===
encoded_bits = viterbi_encode(data_bits)  # should return a list of 0s and 1s
error_rate = args.error_rate  # 2% bit error
num_errors = int(len(encoded_bits) * error_rate)
error_indices = random.sample(range(len(encoded_bits)), num_errors)
for idx in error_indices:
    encoded_bits[idx] ^= 1

encoded_str = ''.join(str(b) for b in encoded_bits)    # convert to string

# === 4. Send over TCP ===
HOST = '192.168.1.20'  # Replace with receiver IP
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(encoded_str.encode(), (HOST, PORT))
    print("[Sender] Sent 32x32 encoded binary data over UDP.")

