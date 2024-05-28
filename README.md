# Reset Voltage Server

This project provides a server application that allows for resetting the bias voltages of MC DAQ (blue boxes) over TCP/IP. The antilatch code allows for multiple blue boxes to be addressed in parallel, and also for individual channels to be reset. The server listens for incoming client connections, processes a restart command, and interacts with the hardware to reset voltage settings as specified by the client.

## File Descriptions

### Server Code
#### `antilatch-server.py`
This file contains the main server code to be run on the computer with the blue boxes. The server listens for incoming connections, processes commands to reset bias voltages, and sends responses back to the client.

#### `antilatch-client.py`
This file contains reads a `configuration.py` file with the optimal bias voltages, and connects to the server through TCP to reset the hardware.

#### `antilatch.py`
This file connects to the blue boxes and resets the bias voltage for the boards and channels specified by the client.

### Dependencies
Just run `pip install -r requirements.txt`

---

## Notes
1. Make sure the `config.py` file is accessible to the client.
2. Change the IP address and open port for the server to use.
