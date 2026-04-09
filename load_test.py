from concurrent.futures import ThreadPoolExecutor
import socket, json

HOST = "127.0.0.1"
PORT = 9000

def client_job(n):
    s = socket.socket()
    s.connect((HOST, PORT))

    msg = {
        "action": "register",
        "data": {
            "sender": f"D{n}",
            "receiver": f"C{n}",
            "address": "DXB",
            "email": f"{n}@mail.com"
        }
    }

    s.send(json.dumps(msg).encode())
    result = json.loads(s.recv(4096).decode())
    s.close()
    return result

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(client_job, range(5)))

print("Results:", results)