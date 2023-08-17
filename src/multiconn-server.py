
# import socket

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()

#     with conn:
#         print(f'Connected by {addr}')
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)
# import sys
# import socket
# import selectors
# import types

# sel = selectors.DefaultSelector()

# host, port = sys.argv[1], int(sys.argv[2])
# lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# lsock.bind((host, port))
# lsock.listen()
# print(f'Listening on {(host, port)}')
# lsock.setblocking(False)
# sel.register(lsock, selectors.EVENT_READ, data=None)

# def accept_wrapper(sock):
#         conn, addr = sock.accept()  # Should be ready to read
#         print(f"Accepted connection from {addr}")
#         conn.setblocking(False)
#         data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
#         events = selectors.EVENT_READ | selectors.EVENT_WRITE
#         sel.register(conn, events, data=data)

# try:
#     while True:
#         events = sel.select(timeout=None)
#         for key, mask in events:
#             if key.data is None:
#                 accept_wrapper(key.fileobj)
#             else:
#                 service_connection(key, mask)
# except KeyboardInterrupt:
#     print("Caught keyboard interrupt, exiting")
# finally:
#     sel.close()




# print(os.getcwd())
# print(os.listdir())
# file_path = "config.txt"
# config = os.path.join('src', 'config.txt')

# with open(config, "r") as config:
#     for line in config:
#         print(line)

    