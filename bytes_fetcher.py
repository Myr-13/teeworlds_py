import threading
import socket

# Local server for connect
local_server_port = 8304
local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_socket.bind(("", local_server_port))
print("Created server at localhost:8304")

# Remote server for send
remote_ip = ("localhost", 8303)
remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
remote_socket.connect(remote_ip)
print("Connected to remote host")


# Main class
class Server:
	client_address = str

	def local(self):
		print("Listening local server")

		while True:
			received_data, received_client = local_socket.recvfrom(2048)
			self.client_address = received_client
			remote_socket.sendto(received_data, remote_ip)

			print("CLIENT:", received_data)

	def remote(self):
		print("Listening remote server")

		while True:
			received_data, received_client = remote_socket.recvfrom(2048)
			local_socket.sendto(received_data, self.client_address)

			print("SERVER:", received_data)

server = Server()
threading.Thread(target=server.local).start()
threading.Thread(target=server.remote).start()
print("Server started, waiting connections")
