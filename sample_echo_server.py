"""
sample_echo_server.py
A very small TCP echo server for CIS 427-style client/server practice.

This example is intentionally simpler than Project 1.  It does not implement
LOGIN, SOLVE, LIST, user files, or authentication.  It only demonstrates:
- creating a TCP socket
- binding to a port
- listening for one client at a time
- receiving newline-terminated text commands
- sending newline-terminated text responses
- handling LOGOUT and SHUTDOWN-style commands
"""

import socket

SERVER_HOST = "127.0.0.1"   # Listen locally for testing on one machine
SERVER_PORT = 4270          # Change if this port is already in use
BUFFER_SIZE = 1024


def handle_client(client_socket, client_address):
    """Receive messages from one client until the client logs out or disconnects."""
    print(f"Client connected from {client_address}")

    with client_socket:
        while True:
            data = client_socket.recv(BUFFER_SIZE)

            if not data:
                print("Client disconnected.")
                return False

            message = data.decode("utf-8").strip()
            print(f"Received from client: {message}")

            if message.upper() == "LOGOUT":
                client_socket.sendall("200 OK\n".encode("utf-8"))
                print("Client logged out.")
                return False

            if message.upper() == "SHUTDOWN":
                client_socket.sendall("200 OK\n".encode("utf-8"))
                print("Shutdown requested.  Server will terminate.")
                return True

            response = f"ECHO: {message}\n"
            client_socket.sendall(response.encode("utf-8"))


def main():
    """Start the TCP server and allow one active client at a time."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)

        print(f"Echo server listening on {SERVER_HOST}:{SERVER_PORT}")
        print("Press Ctrl+C to stop the server manually.\n")

        should_shutdown = False
        while not should_shutdown:
            client_socket, client_address = server_socket.accept()
            should_shutdown = handle_client(client_socket, client_address)

        print("Server stopped.")


if __name__ == "__main__":
    main()
