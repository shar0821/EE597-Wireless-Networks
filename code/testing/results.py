import math

ORIGINAL = "../sender/original_binary_array.txt"
RECEIVED = "../receiver/reconstructed_array.txt"

original_data=list()
received_data=list()

with open(ORIGINAL,'r') as ori:
	for line in ori:
		bits = list(map(int, line.strip().split()))
		original_data.append(bits)

with open(RECEIVED,'r') as rec:
	for line in rec:
		bits = list(map(int, line.strip().split()))
		received_data.append(bits)

print(len(original_data))
print(len(received_data))
total_bits = 32 * 32
error_bits=0
for i in range(32):
	for j in range(32):
		error_bits+=(original_data[i][j]!=received_data[i][j])

ber = error_bits / total_bits

def compute_psnr(original, reconstructed):
    mse = 0.0
    for i in range(32):
        for j in range(32):
            mse += (original[i][j] - reconstructed[i][j]) ** 2
    mse /= (32 * 32)

    if mse == 0:
        return float('inf')  # Perfect match
    psnr = 10 * math.log10((1 ** 2) / mse)  # MAX_I = 1 for binary
    return psnr

psnr = compute_psnr(original_data,received_data)

print(f"Bit Error Rate:{ber}")
print(f"PSNR:{psnr}")
