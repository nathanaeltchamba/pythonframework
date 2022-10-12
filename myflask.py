from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json
from urllib.parse import urlparse

routes = {}
route_methods = {}

class Request:
    def __init__(self, request, method):
        self.request = request
        self.method = method
        self.path = urlparse.urlparse(request.path).path
        self.qs = urlparse.parse_qs(urlparse.urlparse(request.path).query)
        self.headers = request.headers
        self.content_length = int(self.headers.get('content-length', 0))
        self.body = request.rfile.read(self.content_length)
        try:
            self.json = json.loads(self.body)
        except json.decoder.JSONDecodeError: 
            self.json = {}

class Flask:
    def __init__(self):
        pass

    def run(self, server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=8000):
        server_address = ('', port)
        print(f"Running sever in port {port}")
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

    def route(self, path, methods):
        def wrapper(f):
            routes[path] = f
            route_methods[path] = methods
        return wrapper

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str.encode("Handling GET"))
    
    def do_POST(self):
        pass
