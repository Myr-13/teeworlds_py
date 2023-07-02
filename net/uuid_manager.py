from hashlib import md5
from typing import List


def get_tw_md5_hash(name: str):
	_hash = md5()
	_hash.update(bytearray([0xe0, 0x5d, 0xda, 0xaa, 0xc4, 0xe6, 0x4c, 0xfb, 0xb6, 0x42, 0x5d, 0x48, 0xe8, 0x0c, 0x00, 0x29]))
	_hash.update(name.encode())
	hex_hash = _hash.hexdigest()
	_hash = [int(digit, 16) for digit in hex_hash]

	_hash[6] &= 0x0F
	_hash[6] |= 0x30
	_hash[8] &= 0x3F
	_hash[8] |= 0x80

	return bytes(_hash)


class UUID:
	def __init__(self, name: str, _hash: bytes, type_id: int):
		self.name = name
		self.hash = _hash
		self.type_id = type_id


class UUIDManager:
	def __init__(self, offset: int = 65536):
		self.uuids: List[UUID] = []
		self.offset = offset
		self.snapshot = False

	def lookup_hash(self, _hash: bytes):
		for uuid in self.uuids:
			if uuid.hash == _hash:
				return uuid

	def lookup_name(self, name: str):
		for uuid in self.uuids:
			if uuid.name == name:
				return uuid

	def lookup_type(self, type_id: int):
		if not self.snapshot:
			return self.uuids[type_id - self.offset]

		for uuid in self.uuids:
			if uuid.type_id == type_id:
				return uuid

	def register_name(self, name: str, type_id: int = -1):
		if type_id == -1:
			type_id = self.offset - len(self.uuids)

		uuid = UUID(name, get_tw_md5_hash(name), type_id)
		self.uuids.append(uuid)
