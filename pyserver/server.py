from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

MY_MOVIES = ["Avatar", "Inception", "Oppenheimer"]

class MyRequestHandler(BaseHTTPRequestHandler):

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found.", "utf-8"))

    def handleGetMoviesCollection(self):
        # response status code:
        self.send_response(200)
        # response header:
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        # response body:
        self.wfile.write(bytes(json.dumps(MY_MOVIES), "utf-8"))

    def handleCreateMovie(self):
        print("request headers:", self.headers)

        # 1. read the data in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body:", parsed_body)

        # 2. append to MY_MOVIES
        movie_name = parsed_body["name"][0] # index the dictionary & list
        MY_MOVIES.append(movie_name)

        # 3. send a response
        self.send_response(201)
        self.end_headers()

    def do_GET(self):
        if self.path == "/movies":
            self.handleGetMoviesCollection()
        else:
            self.handleNotFound()

    def do_POST(self):
        if self.path == "/movies":
            self.handleCreateMovie()
        else:
            self.handleNotFound()


def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyRequestHandler)

    print("Server running!")
    server.serve_forever()

if __name__ == '__main__':
    run()
