import json
import socket
from urllib.parse import urlparse

from main import save_resource, show_source

HOST = '127.0.0.1'
PORT = 8080

def http_response(status_code, body, locator=None, content_type="text/plain; charset=utf-8"):
    reasons = {
        200: "OK",
        302: "Found",
        400: "Bad Request",
        404: "Not Found",
        405: "Method Not Allowed"
    }

    reason = reasons.get(status_code, "OK")
    location_header = f"Location: {locator}\r\n" if locator else ""

    response = (
        f"HTTP/1.1 {status_code} {reason}\r\n{location_header}"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    return response.encode("utf-8") + body

def handle_request(request_bytes):
    try:
        parts = request_bytes.split(b"\r\n\r\n", 1)
        
        header_bytes = parts[0]
        body_bytes = parts[1] if len(parts[1]) > 1 else b""


        header_text = header_bytes.decode("iso-8859-1")
        header_lines = header_text.split("\r\n")

        request_line = header_lines[0]
        method, target, _ = request_line.split()
        
        parsed = urlparse(target)
        path = parsed.path

        if method == "POST" and path == "/shorten":
            if not body_bytes:
                return http_response(400, b"Empty Body")
            
            data = json.loads(body_bytes.decode("utf-8"))
            alias = save_resource(data['url'])
            
            return http_response(200, f"URL Shortened. You can redirect using http://localhost:8080/{alias}.".encode(), None, "application/json")
        
        if method == "GET" and len(path) > 1:
            alias = path[1:]
            source = show_source(alias)

            return http_response(302, b"URL Found.", source)
        
        return http_response(404, b"Page not found")
    
    except Exception:
        return http_response(400, b"Bad Request")

def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        print(f"Listening on http://{HOST}:{PORT}")

        while True:
            client, _ = server.accept()
            with client:
                request = client.recv(4096)
                response = handle_request(request)
                client.sendall(response)

if __name__ == "__main__":
    serve()