import socket
import sys
import traceback
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

def renderServerErrorPage(err):
    ans = '<link rel="stylesheet" href="/st/css/errorpage.css">'
    ans += "<div><h1>ERROR :(</h1></div>"
    ans += "<p><b>What happened:</b> " + str(sys.exc_info()[1]) + "</p>"
    ans += "<pre>"
    #t = ""
    for elem in traceback.extract_tb(sys.exc_info()[2]).format():
        ans += elem.replace("<", "$").replace(">", "$").replace("\n", "<br>")#.replace("  ", "&nbsp;&nbsp;")
        #t += elem.replace("<", "$").replace(">", "$").replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;") + "\n"
    ans += "</pre>"
    return ans


HOST, PORT = '', 8080

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print('Serving HTTP on port', PORT)
while True:
    try:
        client_connection, client_address = listen_socket.accept()
    except KeyboardInterrupt:
        break
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
            print("[ OK] File request at", path)
        except:
            print("[ERR] No file at", path)
            http_response = HEADERS_404
    else:
        print("[   ] Request page at: '", path, "'...", sep="")
        try:
            page_code = render.main(path)
            http_response = HEADERS_200_HTML + page_code.encode()
            print("[ OK] Request fulfilled successfully")
        except:
            http_response = HEADERS_200_HTML + renderServerErrorPage(sys.exc_info()).encode()
            print("[ERR] Error happened during page render:", sys.exc_info()[1])
            print("      (more info on page)")
    client_connection.sendall(http_response)
    client_connection.close()

print("Server stopped")
