import socket
import json
from datetime import datetime

HOST = "127.0.0.1"
PORT = 9000

database = {}
pkg_counter = 0

ALLOWED_STATUS = ["registered", "picked_up", "in_transit", "delivered"]


def create_package_id():
    global pkg_counter
    pkg_counter += 1
    return f"PKG-{pkg_counter:04d}"


def print_log(text):
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] {text}")


def register(data):
    fields = ["sender", "receiver", "address", "email"]
    for f in fields:
        if f not in data:
            return {"status": "error", "message": f"Missing field: {f}"}

    pid = create_package_id()
    database[pid] = {
        "parcel_id": pid,
        "sender": data["sender"],
        "receiver": data["receiver"],
        "address": data["address"],
        "email": data["email"],
        "status": "registered"
    }

    return {"status": "ok", "parcel_id": pid}


def lookup(data):
    pid = data.get("parcel_id")
    if pid in database:
        return {"status": "ok", "parcel": database[pid]}
    return {"status": "error", "message": "Parcel not found"}


def update(data):
    pid = data.get("parcel_id")
    status = data.get("new_status")

    if pid not in database:
        return {"status": "error", "message": "Parcel not found"}

    if status not in ALLOWED_STATUS:
        return {"status": "error", "message": "Invalid status"}

    database[pid]["status"] = status
    return {"status": "ok", "parcel_id": pid, "new_status": status}


def handle_request(req):
    action = req.get("action")
    data = req.get("data", {})

    if action == "register":
        return register(data)
    elif action == "lookup":
        return lookup(data)
    elif action == "update_status":
        return update(data)
    else:
        return {"status": "error", "message": "Invalid action"}


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print_log("Server started")

    while True:
        conn, addr = server.accept()
        print_log(f"Client {addr} connected")

        try:
            msg = conn.recv(4096).decode()

            if not msg:
                conn.close()
                continue

            try:
                request = json.loads(msg)
            except:
                conn.send(json.dumps({"status": "error", "message": "Bad JSON"}).encode())
                conn.close()
                continue

            response = handle_request(request)
            conn.send(json.dumps(response).encode())

        except Exception as e:
            print_log(f"Error: {e}")

        conn.close()


if __name__ == "__main__":
    run_server()