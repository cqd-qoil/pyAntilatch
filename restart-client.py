# restart-client.py

import socket
import json
from antilatch import restart_boxes
from config import device_id_list, bias_voltage_list

HOST = '127.0.0.1'  # Change to actual IP address/hostname of the server
PORT = 12345  # Change to actual port used by the server

verbose = False # If verbose is True, it will print messages and dump info on you whenever latching happens

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        if verbose:
             print("Connected to server.")
        data_to_send = {
                        "message": "restart",
                        "device_id_list": device_id_list,
                        "bias_voltage_list": bias_voltage_list
                        }
        encoded_data = json.dumps(data_to_send).encode('utf-8')
        s.sendall(encoded_data)

        data = s.recv(1024)
        if verbose:
            print('Received:', data.decode())

if __name__ == "__main__":
    main()
