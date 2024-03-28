from dataclasses import dataclass
from typing import Dict
from urllib.parse import urlparse
import socket
import ssl

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"


@dataclass
class HttpResponse:
    status_code: int
    headers: Dict[str, str]
    body: str


def extract_url_parts(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc, parsed_url.path, parsed_url.query, parsed_url.scheme


def get(url: str) -> HttpResponse:
    url_object = urlparse(url)
    port = 443 if url_object.scheme == "https" else 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the socket with SSL context
    context = ssl.create_default_context()
    sock = context.wrap_socket(
        sock, server_hostname=url_object.netloc) if url_object.scheme == "https" else sock

    sock.connect((url_object.netloc, port))

    request = f"GET {url_object.path}{url_object.query and '?' or ''}{url_object.query} HTTP/1.1\r\n" \
        f"Host: {url_object.netloc}\r\n" \
        f"User-Agent: {USER_AGENT}\r\n" \
        f"Connection: close\r\n\r\n"

    sock.send(request.encode())

    response_buffer = bytes()
    while True:
        data = sock.recv(4096)
        if not data:
            break
        response_buffer += data
    response = response_buffer.decode("utf-8")
    # print(response)
    http_header, http_body = response.split("\r\n\r\n", 1)
    status_line, *headers = http_header.split("\r\n")
    status_code = int(status_line.split(" ")[1])
    headers = dict(header.split(": ", 1) for header in headers)
    if "Location" in headers:
        return get(headers["Location"])
    return HttpResponse(status_code, headers, http_body)


# print(get("http://www.google.com/search?q=python"))
