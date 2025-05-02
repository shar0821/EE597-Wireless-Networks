import socket
from viterbi_encoder import viterbi_encode

# Bitstream to send
data_bits = [1, 0, 1, 1, 0, 1]

# Encode using Viterbi
encoded_bits = viterbi_encode(data_bits)

# Convert to bytes
byte_data = bytes(encoded_bits)

# Send over TCP
HOST = 'receiver_ip'  # Replace with actual IP of Node B
PORT = 9999
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(byte_data)
    print("Data sent.")
