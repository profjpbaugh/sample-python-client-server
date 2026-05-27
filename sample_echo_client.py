"""
sample_echo_client.py
A very small TCP echo client for CIS 427-style client/server practice.

This example connects to sample_echo_server.py, lets the user type messages,
sends each message to the server, and prints the server's response.
"""

import socket

SERVER_HOST = "127.0.0.1"   # Change this to the server machine's IP if needed
SERVER_PORT = 4270          # Must match the server's port
BUFFER_SIZE = 1024


def main():
    """Connect to the server and send user-entered messages."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")
        print("Type messages to send to the server.")
        print("Try: hello")
        print("Try: LOGOUT")
        print("Try: SHUTDOWN\n")

        while True:
            message = input("C: ").strip()

            if not message:
                print("Please enter a message.")
                continue

            client_socket.sendall((message + "\n").encode("utf-8"))

            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print("Server closed the connection.")
                break

            response = data.decode("utf-8").strip()
            print(f"S: {response}")

            if message.upper() in ("LOGOUT", "SHUTDOWN"):
                break

    print("Client stopped.")


if __name__ == "__main__":
    main()
