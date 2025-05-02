# viterbi_encoder.py
def viterbi_encode(data):
    g1 = 0b111
    g2 = 0b101
    encoded = []
    shift_reg = [0, 0, 0]
    for bit in data:
        shift_reg = [bit] + shift_reg[:-1]
        out1 = sum([bit & (g1 >> i & 1) for i, bit in enumerate(shift_reg)]) % 2
        out2 = sum([bit & (g2 >> i & 1) for i, bit in enumerate(shift_reg)]) % 2
        encoded.extend([out1, out2])
    return encoded
