FREQ_TABLE = [1 << 30, 4545, 2657, 431, 1950, 919, 444, 482, 2244, 617, 838, 542, 715, 1814, 304, 240, 754, 212, 647, 186,
	283, 131, 146, 166, 543, 164, 167, 136, 179, 859, 363, 113, 157, 154, 204, 108, 137, 180, 202, 176,
	872, 404, 168, 134, 151, 111, 113, 109, 120, 126, 129, 100, 41, 20, 16, 22, 18, 18, 17, 19,
	16, 37, 13, 21, 362, 166, 99, 78, 95, 88, 81, 70, 83, 284, 91, 187, 77, 68, 52, 68,
	59, 66, 61, 638, 71, 157, 50, 46, 69, 43, 11, 24, 13, 19, 10, 12, 12, 20, 14, 9,
	20, 20, 10, 10, 15, 15, 12, 12, 7, 19, 15, 14, 13, 18, 35, 19, 17, 14, 8, 5,
	15, 17, 9, 15, 14, 18, 8, 10, 2173, 134, 157, 68, 188, 60, 170, 60, 194, 62, 175, 71,
	148, 67, 167, 78, 211, 67, 156, 69, 1674, 90, 174, 53, 147, 89, 181, 51, 174, 63, 163, 80,
	167, 94, 128, 122, 223, 153, 218, 77, 200, 110, 190, 73, 174, 69, 145, 66, 277, 143, 141, 60,
	136, 53, 180, 57, 142, 57, 158, 61, 166, 112, 152, 92, 26, 22, 21, 28, 20, 26, 30, 21,
	32, 27, 20, 17, 23, 21, 30, 22, 22, 21, 27, 25, 17, 27, 23, 18, 39, 26, 15, 21,
	12, 18, 18, 27, 20, 18, 15, 19, 11, 17, 33, 12, 18, 15, 19, 18, 16, 26, 17, 18,
	9, 10, 25, 22, 22, 17, 20, 16, 6, 16, 15, 20, 14, 18, 24, 335, 1517
]

HUFFMAN_EOF_SYMBOL = 256
HUFFMAN_MAX_SYMBOLS = HUFFMAN_EOF_SYMBOL + 1
HUFFMAN_MAX_NODES = HUFFMAN_MAX_SYMBOLS * 2 - 1
HUFFMAN_LUTBITS = 10
HUFFMAN_LUTSIZE = 1 << HUFFMAN_LUTBITS
HUFFMAN_LUTMASK = HUFFMAN_LUTSIZE - 1


class HuffmanNode:
	def __init__(self):
		self.bits = 0
		self.numbits = 0
		self.left = 0
		self.right = 0
		self.symbol = 0


class HuffmanConstructNode:
	def __init__(self):
		self.node_id = 0
		self.frequency = 0


class Huffman:
	def __init__(self, freq = FREQ_TABLE):
		self.nodes = []
		self.decode_lut = []
		self.num_nodes = 0
		self.start_node_index = 0

		for i in range(HUFFMAN_MAX_NODES):
			self.nodes.append(HuffmanNode())
		for i in range(HUFFMAN_LUTSIZE):
			self.decode_lut.append(0)
		
		self.construct_tree(freq)

		for i in range(HUFFMAN_LUTSIZE):
			bits = i
			broke = False
			index = self.start_node_index

			for x in range(HUFFMAN_LUTBITS):
				if bits & 1:
					index = self.nodes[index].right
				else:
					index = self.nodes[index].left
				bits >>= 1

				if self.nodes[index].numbits != 0:
					self.decode_lut[i] = index
					broke = True
					break
			
			if not broke:
				self.decode_lut[i] = index

	def set_bits_r(self, node_index, bits, depth):
		if self.nodes[node_index].right != 0xFFFF:
			self.set_bits_r(self.nodes[node_index].right, bits | (1 << depth), depth + 1)
		if self.nodes[node_index].left != 0xFFFF:
			self.set_bits_r(self.nodes[node_index].left, bits, depth + 1)
		if self.nodes[node_index].numbits != 0:
			self.nodes[node_index].bits = bits
			self.nodes[node_index].numbits = depth

	def bubble_sort(self, index_list, node_list, size):
		changed = True

		while changed:
			changed = False

			for i in range(size - 1):
				if node_list[index_list[i]].frequency < node_list[index_list[i + 1]].frequency:
					temp = index_list[i]
					index_list[i] = index_list[i + 1]
					index_list[i + 1] = temp
					changed = True

			size -= 1

		return index_list

	def construct_tree(self, freq = FREQ_TABLE):
		nodes_left_storage = []
		nodes_left = []
		num_nodes_left = HUFFMAN_MAX_SYMBOLS

		for i in range(HUFFMAN_MAX_SYMBOLS):
			nodes_left_storage.append(HuffmanConstructNode())
			nodes_left.append(0)

		for i in range(HUFFMAN_MAX_SYMBOLS):
			self.nodes[i].symbol = i
			self.nodes[i].numbits = 0xFFFFFFFF
			self.nodes[i].left = 0xFFFF
			self.nodes[i].right = 0xFFFF

			if i == HUFFMAN_EOF_SYMBOL:
				nodes_left_storage[i].frequency = 1
			else:
				nodes_left_storage[i].frequency = freq[i]
			nodes_left_storage[i].node_id = i
			nodes_left[i] = i
		
		self.num_nodes = HUFFMAN_MAX_SYMBOLS

		while num_nodes_left > 1:
			nodes_left = self.bubble_sort(nodes_left, nodes_left_storage, num_nodes_left)
			
			self.nodes[self.num_nodes].numbits = 0
			self.nodes[self.num_nodes].left = nodes_left_storage[nodes_left[num_nodes_left - 1]].node_id
			self.nodes[self.num_nodes].right = nodes_left_storage[nodes_left[num_nodes_left - 2]].node_id
			
			nodes_left_storage[nodes_left[num_nodes_left - 2]].node_id = self.num_nodes
			nodes_left_storage[nodes_left[num_nodes_left - 2]].frequency = nodes_left_storage[nodes_left[num_nodes_left - 1]].frequency + nodes_left_storage[nodes_left[num_nodes_left - 2]].frequency
			self.num_nodes += 1
			num_nodes_left -= 1
		
		self.start_node_index = self.num_nodes - 1
		self.set_bits_r(self.start_node_index, 0, 0)

	def compress(self, inp_buffer, start_index = 0, size = 0):
		output = []
		bits = 0
		bitcount = 0

		if size == 0:
			size = len(inp_buffer)

		inp_buffer = inp_buffer[start_index:start_index+size]

		for i in range(size):
			x = inp_buffer[i]
			bits |= self.nodes[x].bits << bitcount
			bitcount += self.nodes[x].numbits

			while bitcount >= 8:
				output.append(bits & 0xFF)
				bits >>= 8
				bitcount -= 8
		
		bits |= self.nodes[HUFFMAN_EOF_SYMBOL].bits << bitcount
		bitcount += self.nodes[HUFFMAN_EOF_SYMBOL].numbits

		while bitcount >= 8:
			output.append(bits & 0xFF)
			bits >>= 8
			bitcount -= 8
		
		output.append(bits)
		return bytes(output)

	def decompress(self, inp_buffer, size = 0):
		bits = 0
		bitcount = 0
		eof = self.nodes[HUFFMAN_EOF_SYMBOL]
		output = []
		
		if size == 0:
			size = len(inp_buffer)

		src_index = 0
		while True:
			node_i = -1

			if bitcount >= HUFFMAN_LUTBITS:
				node_i = self.decode_lut[bits & HUFFMAN_LUTMASK]

			while bitcount < 24 and src_index != size:
				bits |= inp_buffer[src_index] << bitcount
				bitcount += 8
				src_index += 1
			
			if node_i == -1:
				node_i = self.decode_lut[bits & HUFFMAN_LUTMASK]

			if self.nodes[node_i].numbits:
				bits >>= self.nodes[node_i].numbits
				bitcount -= self.nodes[node_i].numbits
			else:
				bits >>= HUFFMAN_LUTBITS
				bitcount -= HUFFMAN_LUTBITS

				while True:
					if bits & 1:
						node_i = self.nodes[node_i].right
					else:
						node_i = self.nodes[node_i].left

					bitcount -= 1
					bits >>= 1

					if self.nodes[node_i].numbits:
						break
					if bitcount == 0:
						raise Exception("No more bits, decoding error")
			
			if self.nodes[node_i] == eof:
				break

			output.append(self.nodes[node_i].symbol)

		return bytes(output)
