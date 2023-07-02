from typing import List

from .chunk import Chunk
from .huffman import Huffman


class Packet:
	def __init__(self) -> None:
		self.flags = 0
		self.ack = 0
		self.chunkCount = 0
		self.size = 0
		self.chunks = []

	def unpack(self, _bytes: bytes, huffman: Huffman):
		self.flags = _bytes[0] >> 4
		self.ack = ((_bytes[0] & 0xF) << 8) | _bytes[1]
		self.chunkCount = _bytes[2]
		self.size = len(_bytes) - 3
		packet = _bytes[3:]

		# Decompress flag
		if self.flags & 8 and not self.flags & 1:
			packet = huffman.decompress(packet)
			if len(packet) and packet[0] != -1:
				return

		# Get chunks
		for i in range(self.chunkCount):
			chunk = Chunk()

			# Get len of data & flags
			b = ((packet[0] & 0x3F) << 4) | (packet[1] & ((1 << 4) - 1))
			chunk.flags = (packet[0] >> 6) & 3

			# Sequence
			if chunk.flags & 1:
				chunk.sequence = ((packet[1] & 0xF0) << 2) | packet[2]
				packet = packet[3:]  # Remove flags & size
			else:
				packet = packet[2:]

			# Get info
			chunk.sys = bool(packet[0] & 1)
			chunk.msgid = round((packet[0] - (packet[0] & 1)) / 2)
			chunk.raw = packet[1:b]

			# Add chunk to packet
			self.chunks.append(chunk)

			# Goto next chunk
			packet = packet[b:]

	def pack(self, chunks: List[Chunk]) -> bytes:
		self.chunks = chunks
		chunks = b""

		# Pack all chunks
		for c in self.chunks:
			header = []
			header_len = 2
			if c.flags & 1:
				header_len = 3

			# Allocate header
			for i in range(header_len):
				header.append(0)

			header[0] = ((c.flags & 3) << 6) | ((c.size >> 4) & 0x3F)
			header[1] = (c.size & 0xF)

			if c.flags & 1:
				self.ack = (self.ack + 1) % (1 << 10)

				header[1] |= (self.ack >> 2) & 0xF0
				header[2] = self.ack & 0xFF
				header[0] = (((c.flags | 2) & 3) << 6) | ((c.size >> 4) & 0x3F)

			# Pack chunk
			chunks += bytes(2 * c.msgid + int(c.sys))
			chunks += bytes(header)
			chunks += c.raw

		# Pack packet
		packet_header = [
			((self.flags << 4) & 0xF0) | ((self.ack >> 8) & 0xF),
			self.ack & 0xFF,
			len(self.chunks)
		]

		packet = bytes(packet_header) + chunks

		return packet
