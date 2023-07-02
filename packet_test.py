# Test for network packets

from net.packet import Packet
from net.chunk import Chunk
from net.huffman import Huffman

p = Packet()

c = Chunk()
c.msgid = 0
c.sys = False
c.add_str("keko")
c.add_int(123321)
c.add_str("hehe")

pack = p.pack([c])
print(f"Packed: {pack}")
p.unpack(pack, Huffman())

c = p.chunks[0]
print(f"Chunk: {c}")
print("Packed data:")
print(c.get_str())
print(c.get_int())
print(c.get_str())
