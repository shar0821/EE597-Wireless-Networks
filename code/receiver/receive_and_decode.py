import socket

# === Viterbi Decoder Function ===
def viterbi_decode(received_bits):
    g1 = 0b111
    g2 = 0b101
    states = ['00', '01', '10', '11']
    
    def shift_and_encode(state, input_bit):
        reg = [int(input_bit)] + [int(b) for b in state]
        out1 = sum([reg[i] & (g1 >> i & 1) for i in range(3)]) % 2
        out2 = sum([reg[i] & (g2 >> i & 1) for i in range(3)]) % 2
        next_state = str(reg[0]) + str(reg[1])
        return next_state, f"{out1}{out2}"

    path_metrics = {'00': (0, '')}

    for i in range(0, len(received_bits), 2):
        symbol = received_bits[i:i+2]
        new_metrics = {}

        for state in states:
            for input_bit in ['0', '1']:
                prev_state = state
                next_state, expected = shift_and_encode(state, input_bit)

                if prev_state in path_metrics:
                    prev_metric, path = path_metrics[prev_state]
                    hamming = sum(a != b for a, b in zip(symbol, expected))
                    metric = prev_metric + hamming

                    if next_state not in new_metrics or metric < new_metrics[next_state][0]:
                        new_metrics[next_state] = (metric, path + input_bit)

        path_metrics = new_metrics

    best_state = min(path_metrics, key=lambda k: path_metrics[k][0])
    return path_metrics[best_state][1]

# === Socket Server to Receive Encoded Data ===
HOST = '0.0.0.0'
PORT = 9000


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print("[Receiver] Listening for UDP packets on port 9999...")

    data, addr = s.recvfrom(65535)  # large buffer for UDP
    print(f"[Receiver] Received packet from {addr}")

encoded_bits = data.decode().strip()
print(f"[Receiver] Received {len(encoded_bits)} bits.")

# === 2. Decode using Viterbi ===
decoded_bits = viterbi_decode(encoded_bits)  # string of 0s and 1s
print(f"[Receiver] Decoded to {len(decoded_bits)} bits.")

# === 3. Convert bitstream back to 32x32 binary array ===
if len(decoded_bits) < 1024:
    raise ValueError("Decoded data too short! Expected 1024 bits.")

binary_array = [[int(decoded_bits[row * 32 + col]) for col in range(32)] for row in range(32)]

# === 4. Save reconstructed array as text ===
with open("reconstructed_array.txt", "w") as f:
    for row in binary_array:
        f.write(' '.join(str(bit) for bit in row) + '\n')

print("[Receiver] 32x32 binary array reconstructed and saved as reconstructed_array.txt")

