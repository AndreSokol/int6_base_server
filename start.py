import socket
import page_renderer as render

# headers

HEADERS_200_HTML = b"""
HTTP/1.1 200 OK
Server: SimplePyServer (AndreSokol)
Content-Type: text/html; charset=utf-8
Connection: Closed

"""

HEADERS_200_FILE = b"""
HTTP/1.1 200 OK
Server: SimplePyServer (AndreSokol)
Connection: Closed

"""

HEADERS_404 = b"""
HTTP/1.1 404 OK
Server: SimplePyServer (AndreSokol)
Connection: Closed
"""

# code

HOST, PORT = '', 8080

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print('Serving HTTP on port', PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)

    try:
        path = request.split()[1].decode('utf-8')
    except:
        # Sometimes empty requests come, skip'em
        client_connection.close()
        continue
    if path[:4] == "/st/":
        try:
            fileToSend = open("static/" + path[4:], "rb")
            http_response = HEADERS_200_FILE + fileToSend.read()
            fileToSend.close()
            print("Resolved file request at", path)
        except:
            print("unsuccessfully tried to open", path)
            http_response = HEADERS_404
    else:
        print("Request page at: '", path, "'", sep="")
        page_code = render.main(path)
        http_response = HEADERS_200_HTML + page_code.encode()
    client_connection.sendall(http_response)
    client_connection.close()
