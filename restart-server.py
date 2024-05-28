# restart-server.py

import socket
import json
from antilatch import restart_boxes, test_boxes

HOST = '127.0.0.1'  # Change to actual IP address/hostname
PORT = 12345  # Change to actual port used

def jsonKeys2int(x):
    """"
    Convert JSON dictionary keys to integers if they are digit strings. This function is needed because python dictionaries can have integers as keys, but JSON dictionaries cannot.
    """
    if isinstance(x, dict):
        return {int(k):v for k,v in x.items()}
    return x

def handle_client(conn, addr):
    """
    Handle the client connection.
    This function receives data from a connected client, processes it, and sends back a response.
    """
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        decoded_data = json.loads(data)
        decoded_data['bias_voltage_list'] = jsonKeys2int(decoded_data['bias_voltage_list'])
        # Only restart the bias voltage for the corresponding channels if the JSON data received from the client
        # matches expected message and formatting.
        if decoded_data['message'] == "restart":
            val = restart_boxes(device_id_list=decoded_data['device_id_list'],
                                bias_voltage_list=decoded_data['bias_voltage_list'])
            # Send back list of channels and voltages updated
            encoded_list = json.dumps(val).encode('utf-8')
            conn.sendall(encoded_list)
        else:
            conn.sendall(data)

def main():
    """
    Main function to start the server.
    This function sets up the server to listen for incoming connections and handle them using handle_client.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) # Start server at selected HOST address and PORT
        s.listen() # Listen for connections
        print("Server listening on port", PORT)
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    main()
