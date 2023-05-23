import time
import socket
import threading
import socketserver


class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        close = False
        while not close:
            raw_data = self.request.recv(1024)
            data = raw_data.decode().strip()
            if data == "":
                close = True
            else:
                # print("{} wrote: {}".format(self.client_address, data))
                self.request.send(raw_data.decode().upper().encode())


class UDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        raw_data, sock = self.request
        sock.sendto(raw_data.decode().upper().encode(), self.client_address)


class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class UDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


def detect_port(host, port, proto):
    if proto == "tcp":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((host, port))
                sock.sendall("hello\n".encode())
                received = sock.recv(1024).decode()
                if received.strip() == "HELLO":
                    print("[{}] {} {} SUCCESS".format(proto, host, port))
                else:
                    print("\033[1;31m[{}] {} {} FAILED: WRONG ECHO\033[0;0m".format(proto, host, port))
            except OSError as err:
                print("\033[1;31m[{}] {} {} FAILED: {}\033[0;0m".format(proto, host, port, err))
    else:
        # UDP
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Set time to 10s
            sock.settimeout(10)
            sock.sendto("hello\n".encode(), (host, port))
            received = sock.recv(1024).decode()
            if received.strip() == "HELLO":
                print("[{}] {} {} SUCCESS".format(proto, host, port))
            else:
                print("\033[1;31m[{}] {} {} FAILED: WRONG ECHO\033[0;0m".format(proto, host, port))
        except socket.timeout as err:
            print("\033[1;31m[{}] {} {} FAILED: {}\033[0;0m".format(proto, host, port, err))


if __name__ == "__main__":
    target_hosts = [
        "172.16.66.6",
        "172.16.66.10",
    ]

    swarm_ports = {
        #"tcp": [2377, 7946, 26500, 26501, 80, 443],
        "tcp": [10086, 10000],
        #"udp": [24789, 7946]
        "udp": [24789]
    }

    tcp_servers = []
    udp_servers = []
    for proto, ports in swarm_ports.items():
        for port in ports:
            if proto == "tcp":
                tcp_svr = TCPServer(("", port), TCPRequestHandler)
                tcp_svr.allow_reuse_address = True
                tcp_svr_thread = threading.Thread(target=tcp_svr.serve_forever)
                tcp_svr_thread.daemon = True
                tcp_servers.append(tcp_svr_thread)
            else:
                udp_svr = UDPServer(("", port), UDPRequestHandler)
                udp_svr_thread = threading.Thread(target=udp_svr.serve_forever)
                udp_svr_thread.daemon = True
                udp_servers.append(udp_svr_thread)

    for tcp in tcp_servers:
        tcp.start()

    for udp in udp_servers:
        udp.start()

    while True:
        print("====================================")
        for host in target_hosts:
            for proto, ports in swarm_ports.items():
                for port in ports:
                    detect_port(host, port, proto)
        time.sleep(2)
