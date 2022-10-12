from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

routes = {}
route_methods = {}

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
