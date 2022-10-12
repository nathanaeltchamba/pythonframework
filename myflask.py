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

    def write_response(self, response, status_code):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if isinstance(response, dict):
            response = json.dumps(response)
        self.wfile.write(str.encode(response))

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
    def not_found(self, request):
        return self.write_response(f"{request.path} 404 NOT FOUND", 404)

    def method_not_supported(self, request):
        return self.write_response(f"{request.path} {request.method} not supported", 401)
        
    def process_request(self, request):
        if request.path not in routes:
            return self.not_found(request)
        if request.method in route_methods[request.path]:
            return self.method_not_supported(request)
        
        resp = routes[request.path](request)
        self.write_response(resp)
    
            
    def do_GET(self):
        request = Request(self, method='GET')
        return self.process_request(request)

    def do_POST(self):
        request = Request(self, method='POST')
        return self.process_request(request)
