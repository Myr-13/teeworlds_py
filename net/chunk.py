class Chunk:
	def __init__(self, msg_id: int = 0, sys: bool = False, flags: int = 0):
		self.msgid = msg_id
		self.sys = sys
		self.raw = b""
		self.sequence = -1
		self.flags = flags

	def __str__(self) -> str:
		return f"Chunk({self.msgid}): {self.sys} {self.raw} {self.sequence}"

	def get_int(self) -> int:
		index = 0
		sign = ((self.raw[index] >> 6) & 1)
		result = (self.raw[index] & 0b0011_1111)

		while index <= 4:
			if (self.raw[index] & 0b1000_0000) == 0:
				break

			index += 1
			result |= (self.raw[index] & 0b0111_1111) << (6 + 7 * (index - 1))
		
		result ^= -sign

		self.raw = self.raw[index+1:]
		return result

	def get_str(self) -> str:
		result = self.raw[:self.raw.index(b"\x00")]
		self.raw = self.raw[len(result)+1:]
		return result.decode()

	def add_str(self, string: str):
		self.raw += string.encode() + b"\x00"

	def add_raw(self, _bytes: bytes):
		self.raw += _bytes

	def add_int(self, i: int):
		result = []
		dst = (i >> 25) & 0x40
		i ^= (i >> 31)

		dst |= i & 0x3F
		i >>= 6

		if i != 0:
			dst |= 0x80
			result.append(dst)

			while True:
				dst += 1
				dst = i & 0x7F
				i >>= 7
				dst |= (int(i != 0)) << 7

				result.append(dst)

				if i == 0:
					break
		else:
			result.append(dst)

		self.raw += bytes(result)

	@property
	def size(self) -> int:
		return len(self.raw)
