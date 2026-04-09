import socket
import json

HOST = "127.0.0.1"
PORT = 9000


def communicate(message):
    try:
        client = socket.socket()
        client.connect((HOST, PORT))
        client.send(json.dumps(message).encode())

        reply = client.recv(4096).decode()
        client.close()

        return json.loads(reply)
    except:
        print("Cannot connect to server")
        return None


print("Registering...")
res = communicate({
    "action": "register",
    "data": {
        "sender": "Driver1",
        "receiver": "Sara",
        "address": "Dubai Marina",
        "email": "sara@mail.com"
    }
})

print(res)

pid = res["parcel_id"]

print("\nChecking parcel:")
print(communicate({"action": "lookup", "data": {"parcel_id": pid}}))

print("\nUpdating status:")
print(communicate({
    "action": "update_status",
    "data": {"parcel_id": pid, "new_status": "in_transit"}
}))

print("\nFinal check:")
print(communicate({"action": "lookup", "data": {"parcel_id": pid}}))