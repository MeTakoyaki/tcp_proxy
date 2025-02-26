import sys
import socket
import threading

HEX_FILTER=''.join([chr(i) if 32 <= i < 127 else '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = '.'.join([chr(b) if 32 <= b < 127 else '.' for b in src])
        results = []
    for i in range(0, len(src), length):
        word = str(src[i:i+length]) 
        hexa = ' '.join(f'{ord(c):02x}' for c in word)
        hexwidth = length*3
        results.append(f'{i:04x} {hexa:{hexwidth}} {word}')
    if show:
        for line in results:
            print(line)
    return results
                
def receive_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data :
                break
            buffer += data
    except Exception as e:
        print(f"Error receiving data : {e}")
    return buffer

def request_handler(buffer):
    # melakukan modifikasi paket
    return buffer

def response_handler(buffer):
    # melakukan modifikasi paket 
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    remote_buffer=b""
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print =  (f"[==>] Received {len(local_buffer)} bytes from localhost.")
            hexdump(local_buffer)
            local_buffer=request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print(f"[<==] Received {len(remote_buffer)} bytes from remote.")
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("Problem on bind: {e}")
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print(f"[*] Listening on {local_host}:{local_port}")
    server.listen(3)

    while True:
        client_socket, addr = server.accept()
        # mencetak informasi koneksi lokal
        print(f"> Received incoming connection from {addr[0]}:{addr[1]}")

        # memulai sebuah thread untuk berbicara dengan remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print("Usage : ./tcp-proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./tcp-proxy 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5].lower() == "true"

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()
