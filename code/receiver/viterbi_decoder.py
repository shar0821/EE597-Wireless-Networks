# viterbi_decoder.py

import numpy as np

# State transition table for K=3, rate 1/2 encoder
class ViterbiDecoder:
    def __init__(self):
        self.states = [0, 1, 2, 3]  # 2^(K-1)
        self.paths = {s: {'metric': float('inf'), 'path': []} for s in self.states}
        self.paths[0]['metric'] = 0  # Initial state

        self.transition_table = {
            0: {0: (0, [0, 0]), 1: (2, [1, 1])},
            1: {0: (0, [1, 0]), 1: (2, [0, 1])},
            2: {0: (1, [1, 1]), 1: (3, [0, 0])},
            3: {0: (1, [0, 1]), 1: (3, [1, 0])},
        }

    def hamming_distance(self, a, b):
        return sum([bit1 != bit2 for bit1, bit2 in zip(a, b)])

    def decode(self, received_bits):
        steps = len(received_bits) // 2
        for i in range(steps):
            bit_pair = received_bits[2 * i: 2 * i + 2]
            new_paths = {s: {'metric': float('inf'), 'path': []} for s in self.states}
            for state in self.states:
                if self.paths[state]['metric'] < float('inf'):
                    for input_bit in [0, 1]:
                        next_state, expected = self.transition_table[state][input_bit]
                        dist = self.hamming_distance(expected, bit_pair)
                        new_metric = self.paths[state]['metric'] + dist
                        if new_metric < new_paths[next_state]['metric']:
                            new_paths[next_state]['metric'] = new_metric
                            new_paths[next_state]['path'] = self.paths[state]['path'] + [input_bit]
            self.paths = new_paths

        # Find best final state
        final_state = min(self.paths, key=lambda s: self.paths[s]['metric'])
        return self.paths[final_state]['path']


# Example usage
if __name__ == "__main__":
    import sys
    with open(sys.argv[1], 'rb') as f:
        data = list(f.read())
    decoder = ViterbiDecoder()
    decoded = decoder.decode(data)
    print("Decoded bits:", decoded)
