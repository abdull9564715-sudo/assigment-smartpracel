# SmartParcel - NET 214 Assignment

## Student Information
- **Student Name:** abdullatif alhammadi
- **Student ID:** 20220002310
- **CUD Email:** 20220002310@students.cud.ac.ae
- **Course:** NET 214 - Network Programming
- **Semester:** Spring 2026

## Project Description
This project is a simple SmartParcel system built using Python socket programming. It demonstrates TCP client-server communication, parcel registration and tracking, concurrent client handling using threads, and a UDP health check feature.

## Files Included
- `server.py` - TCP server (single-threaded)
- `client.py` - TCP client that demonstrates register, lookup, update_status, and error handling
- `threaded_server.py` - Multi-threaded TCP server with UDP health check
- `load_test.py` - Concurrent test with 5 clients
- `udp_ping.py` - UDP health check client
- `report.pdf` - Assignment report with screenshots, explanations, and architecture diagram

## Requirements
- Python 3

## How to Run
- Run `server.py` to start the TCP server on port 9000.
- Run `client.py` to test parcel registration, lookup, status update, and error handling.
- Run `threaded_server.py` to start the multi-threaded server and UDP listener.
- Run `load_test.py` to test 5 concurrent client registrations.
- Run `udp_ping.py` to test the UDP health check on port 9001.

## Expected Output
- `server.py` should listen on port 9000 and handle client requests correctly.
- `client.py` should show register, lookup, update, and error cases.
- `threaded_server.py` should show TCP and UDP listeners running.
- `load_test.py` should show 5/5 successful concurrent registrations.
- `udp_ping.py` should show server health status and uptime.

## Notes
- TCP is used for parcel operations because it is reliable and ordered.
- UDP is used for health checks because it is lightweight and fast.
- Parcel data is stored in memory using a Python dictionary.

## Author
abdullatif alhammadi
