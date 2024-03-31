import argparse
import logging
import socketserver

# Handler for TCP connections. Just sends back received data, but upper-cased
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip()
        logging.info(f"received from {self.client_address[0]}: {data}")
        self.request.sendall(data.upper())

# Handler for UDP connections. Just sends back received data, but upper-cased
class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        logging.info(f"received from {self.client_address[0]}: {data}")
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    parser = argparse.ArgumentParser(description="microserver for testing connection.")
    parser.add_argument("server_type", type=str, help="server type (tcp or udp)")
    args = parser.parse_args()
    server_type = args.server_type

    logging.info(f"server type: {server_type}")
    HOST, PORT = "localhost", 10000
    # Check server type and try to run the server
    # this will keep running until interrupt with Ctrl-C
    if server_type == "tcp":
        tcp_server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        try:
            tcp_server.serve_forever()
            logging.info("TCP server started")
        except KeyboardInterrupt:
            logging.info("keyboard interruption, server will be stopped")
        finally:
            # Clean up the socket
            tcp_server.shutdown()
            logging.info("server stopped")
    elif server_type == "udp":
        udp_server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
        try:
            udp_server.serve_forever()
            logging.info("UDP server started")
        except KeyboardInterrupt:
            logging.info("keyboard interruption, server will be stopped")
        finally:
            # Clean up the socket
            udp_server.shutdown()
            logging.info("server stopped")
    else:
        logging.error(f"server type is not supported. entered type: {server_type}")
        exit(1)
