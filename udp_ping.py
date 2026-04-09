import socket, json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"ping", ("127.0.0.1", 9001))

data, _ = sock.recvfrom(1024)
print("Response:", json.loads(data.decode()))