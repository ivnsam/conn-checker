#!/bin/python3

import logging
import argparse
import socket

def tcp_check(host, port, timeout=3):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout) # Set a timeout for the connection attempt
    message = b'Hello, Server!'

    try:
        # Attempt to connect to the host and port
        sock.connect((host, port))
        sock.sendall(message)
        data, _ = sock.recvfrom(1024)
        logging.info(f"TCP Connection to {host}:{port} successful.")
        logging.info(f"received {data}")
        return True
    except socket.error as e:
        logging.error(f"TCP Connection to {host}:{port} failed: {e}")
        return False
    finally:
        # Close the socket
        sock.close()


def udp_check(host, port, timeout=3):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout) # Set a timeout
    message = b'Hello, Server!'

    try:
        # Send a message to the server
        sock.sendto(message, (host, port))

        # Receive a response from the server
        data, _ = sock.recvfrom(4096)
        logging.info(f"received {data}")
        logging.info(f"UDP Connection to {host}:{port} successful.")
        return True
    except socket.error as e:
        logging.error(f"UDP connection to {host}:{port} failed: {e}")
        return False
    finally:
        # Close the socket
        sock.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    parser = argparse.ArgumentParser(description="microclient for testing connection.")
    parser.add_argument("connection_type", type=str, help="connection type (tcp or udp)")
    args = parser.parse_args()
    connection_type = args.connection_type
    host = "localhost"
    port = 10000
    timeout = 2
    logging.info(f"connection type: {connection_type}")

    try:
        if connection_type == "tcp":
            check_result = tcp_check(host, port, timeout)
        elif connection_type == "udp":
            check_result = udp_check(host, port, timeout)
        else:
            logging.error(f"connection type is not supported. entered type: {connection_type}")
            exit(1)
        logging.info(f"check result: {check_result}")
    except KeyboardInterrupt:
        logging.info("keyboart interruption, request aborted")
        exit(1)
