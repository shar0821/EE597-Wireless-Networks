import pyshark
from viterbi_decoder import ViterbiDecoder

cap = pyshark.LiveCapture(interface='eth0', display_filter='tcp.port == 9999')

print("Listening for packets...")
for pkt in cap.sniff_continuously(packet_count=1):
    try:
        raw = pkt.tcp.payload.replace(":", "")  # Hex payload string
        byte_data = bytes.fromhex(raw)
        received_bits = list(byte_data)

        decoder = ViterbiDecoder()
        decoded = decoder.decode(received_bits)
        print("Decoded Message:", decoded)
    except Exception as e:
        print("Error decoding:", e)
