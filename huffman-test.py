# Test for huffman

from net.huffman import Huffman

h = Huffman()

b = h.compress(b"Hello world!")
print(f"Compressed data: {b}")
ub = h.decompress(b)
print(f"Decompressed data: {ub}")
