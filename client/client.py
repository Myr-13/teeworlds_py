from typing import Union, Tuple
import socket
import time
import random

from net.packet import *
from net.const import *


def addr_to_tuple(s: str):
	_s = s.split(":")
	return (_s[0], int(_s[1]))


class TwClient:
	def __init__(self):
		self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_address: Tuple[str, int] = ("", 0)
		self.ack = 0
		self.tken = b"\xFF\xFF\xFF\xFF"
		self.huffman = Huffman()

		self.socket.setblocking(True)

	def _send_raw_packet(self, data: bytes):
		self.socket.sendto(data, self.server_address)

		print("CLIENT:", data)

	def send_msg(self, data: Union[List[Chunk], Chunk], flags=0):
		msgs = []
		if isinstance(data, list):
			msgs = data
		else:
			msgs = [data]

		packet = Packet()
		packet.ack = self.ack
		packet.flags = flags
		self._send_raw_packet(packet.pack(msgs))

	def send_control_msg(self, msg_id: int, extra_msg: bytes = b""):
		msg = [
			0x10 + (((16 << 4) & 0xF0) | ((self.ack >> 8) & 0xF)),
			self.ack & 0xFF,
			0x00,
			msg_id
		]
		msg = bytes(msg) + extra_msg + self.tken

		self._send_raw_packet(msg)

	def connect(self, address: str):
		self.server_address = addr_to_tuple(address)

		# Send handshake
		self.send_control_msg(NET_CTRLMSG_CONNECT, b"TKEN")

		while True:
			# time.sleep(1 / self.fps)

			self.update()

	def update(self):
		# Pump network
		data, addr = self.socket.recvfrom(2048)
		self._on_message(data)

	def _process_server_packet(self, chunk: Chunk):
		msg_id = chunk.msgid
		print("CHUNK:", chunk.msgid)

		# System message
		if chunk.sys:
			if msg_id == NETMSG_MAP_CHANGE:
				# TODO: Add map downloader
				self.send_msg(Chunk(NETMSG_READY, True, 1))
			elif msg_id == NETMSG_MAP_DATA:
				pass
			elif msg_id == NETMSG_PING:
				self.send_msg(Chunk(NETMSG_PING_REPLY, True, 0))
			elif msg_id == NETMSG_CON_READY:
				info = Chunk(NETMSGTYPE_CL_STARTINFO, False, 1)
				info.add_str("nameless bot")  # Name
				info.add_str("no clan")  # Clan
				info.add_int(-1)  # Country
				info.add_string("default")  # Skin
				info.add_int(0)  # Use custom colors
				info.add_int(0)  # Color dody
				info.add_int(0)  # Color feet

				crashmplex = Chunk(NETMSG_RCON_CMD, True, 1)
				crashmplex.add_str("crashmplex")

				self.send_msg([info, crashmplex])
			elif msg_id >= NETMSG_SNAP and msg_id <= NETMSG_SNAPSINGLE:
				pass

	def _on_message(self, data: bytes):
		print("SERVER:", data)

		# Check if packet is control
		if data[0] == 0x10:
			# Check if packet is handshake
			if data[3] == NET_CTRLMSG_CONNECTACCEPT:
				self.tken = bytes(data[8:])

				# Send 2 times cuz with 1 time server not responding
				for i in range(2):
					self.send_control_msg(3)  # Accept

				info = Chunk(1, True, 1)
				info.add_str("0.6 626fce9a778df4d4")  # Net version
				info.add_str("")  # Password

				ver = Chunk(0, True, 1)
				ver.add_raw(b"\x8c\x00\x13\x04\x84\x61\x3e\x47\x87\x87\xf6\x72\xb3\x83\x5b\xd4")  # Idk what is it
				ver.add_raw(random.randbytes(16))
				ver.add_int(16050)
				ver.add_str("DDNet 16.5.0")

				self.send_msg([info, ver])
			elif data[3] == NET_CTRLMSG_CLOSE:
				print("disconnected")
			elif data[3] == NET_CTRLMSG_KEEPALIVE:
				pass

			return
		
		# Game packet
		packet = Packet()
		packet.unpack(data, self.huffman)

		for chunk in packet.chunks:
			self._process_server_packet(chunk)
