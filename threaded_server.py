import socket
import json
import threading
import time

HOST = "127.0.0.1"
TCP_PORT = 9000
UDP_PORT = 9001

# Shared data
parcels = {}
counter = 0
lock = threading.Lock()
start_time = time.time()

VALID = ["registered", "picked_up", "in_transit", "delivered"]


# Generate parcel ID safely
def generate_id():
    global counter
    with lock:
        counter += 1
        return f"PKG-{counter:04d}"


# Handle client request
def process_request(req):
    action = req.get("action")
    data = req.get("data", {})

    if action == "register":
        required = ["sender", "receiver", "address", "email"]
        for field in required:
            if field not in data:
                return {"status": "error", "message": f"Missing field: {field}"}

        pid = generate_id()

        with lock:
            parcels[pid] = {
                "parcel_id": pid,
                "sender": data["sender"],
                "receiver": data["receiver"],
                "address": data["address"],
                "email": data["email"],
                "status": "registered"
            }

        return {"status": "ok", "parcel_id": pid}

    elif action == "lookup":
        pid = data.get("parcel_id")

        with lock:
            if pid in parcels:
                return {"status": "ok", "parcel": parcels[pid]}

        return {"status": "error", "message": "Parcel not found"}

    elif action == "update_status":
        pid = data.get("parcel_id")
        new_status = data.get("new_status")

        with lock:
            if pid not in parcels:
                return {"status": "error", "message": "Parcel not found"}

            if new_status not in VALID:
                return {"status": "error", "message": "Invalid status"}

            parcels[pid]["status"] = new_status

        return {"status": "ok", "parcel_id": pid, "new_status": new_status}

    return {"status": "error", "message": "Invalid action"}


# Handle each TCP client
def handle_client(conn, addr):
    try:
        data = conn.recv(4096).decode()

        if not data:
            return

        try:
            request = json.loads(data)
        except:
            conn.send(json.dumps({"status": "error", "message": "Bad JSON"}).encode())
            return

        response = process_request(request)
        conn.send(json.dumps(response).encode())

    except Exception as e:
        print(f"Error with {addr}: {e}")

    finally:
        conn.close()


# UDP Health Check Server
def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, UDP_PORT))

    print(f"UDP server running on {HOST}:{UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)

        uptime = int(time.time() - start_time)

        response = {
            "status": "healthy",
            "uptime": uptime
        }

        sock.sendto(json.dumps(response).encode(), addr)


# Main server
def main():
    # Start UDP in background
    threading.Thread(target=udp_server, daemon=True).start()

    # TCP server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, TCP_PORT))
    server.listen()

    print(f"Threaded TCP server running on {HOST}:{TCP_PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Client {addr} connected")

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()