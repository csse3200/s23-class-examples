from http.server import BaseHTTPRequestHandler, HTTPServer
import json

MY_MOVIES = ["Avatar", "Inception", "Oppenheimer"]

class MyRequestHandler(BaseHTTPRequestHandler):

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found.", "utf-8"))

    def do_GET(self):
        if self.path == "/movies":
            # response status code:
            self.send_response(200)
            # response header:
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # response body:
            self.wfile.write(bytes(json.dumps(MY_MOVIES), "utf-8"))
        else:
            self.handleNotFound()


def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyRequestHandler)

    print("Server running!")
    server.serve_forever()

if __name__ == '__main__':
    run()
