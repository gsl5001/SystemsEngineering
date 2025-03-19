from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    image_data = None
    matrix_data = None

    def do_PUT(self):
        if self.path == '/image':
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                pdict['CONTENT-LENGTH'] = int(self.headers['content-length'])
                fields = cgi.parse_multipart(self.rfile, pdict)
                if 'file' in fields:
                    SimpleHTTPRequestHandler.image_data = fields['file'][0]
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'Image uploaded successfully')
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'No file part in the request')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Content-Type not supported')
        elif self.path == '/matrix':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                SimpleHTTPRequestHandler.matrix_data = json.loads(post_data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Matrix uploaded successfully')
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid JSON format')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

    def do_GET(self):
        if self.path == '/image':
            if SimpleHTTPRequestHandler.image_data is not None:
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(SimpleHTTPRequestHandler.image_data)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Image not found')
        elif self.path == '/matrix':
            if SimpleHTTPRequestHandler.matrix_data is not None:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(SimpleHTTPRequestHandler.matrix_data).encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Matrix not found')
        elif self.path == '/reset':
            SimpleHTTPRequestHandler.image_data = None
            SimpleHTTPRequestHandler.matrix_data = None
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Server reset successfully')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

    def do_POST(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Endpoint not found')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
