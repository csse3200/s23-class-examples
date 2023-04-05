from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
from movies_db import MoviesDB
from passlib.hash import bcrypt
from session_store import SessionStore
import json

SESSION_STORE = SessionStore()

class MyRequestHandler(BaseHTTPRequestHandler):

    def end_headers(self):
        self.sendCookie()
        super().end_headers()

    # read cookie data from the Cookie header
    def loadCookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    # send cookie data using the Set-Cookie header
    def sendCookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def loadSession(self):
        # load the cookie data
        self.loadCookie()
        # check for existance of the session ID cookie
        if 'sessionId' in self.cookie: # if it exists:
            sessionId = self.cookie['sessionId'].value
            # load the session data for the session ID
            self.sessionData = SESSION_STORE.getSessionData(sessionId)
            # if the session ID is not valid:
                # create a new session / session ID
                # save the new session ID into a cookie
                self.cookie['sessionId'] = sessionId
                # load the session with the new session ID
                self.sessionData = SESSION_STORE.getSessionData(sessionId)
        # else:
            # create a new session / session ID
            # save the new session ID into a cookie
            # load the session with the new session ID

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found.", "utf-8"))

    def handleGetMoviesCollection(self):
        #print("headers:", self.headers)

        db = MoviesDB()
        allMovies = db.getAllMovies()

        # response status code:
        self.send_response(200)
        # response header:
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        #self.send_header("Set-Cookie", "flavor=biscoff")
        self.end_headers()
        # response body:
        self.wfile.write(bytes(json.dumps(allMovies), "utf-8"))

    def handleGetMoviesMember(self, movie_id):
        db = MoviesDB()
        oneMovie = db.getOneMovie(movie_id)

        if oneMovie != None:
            # response status code:
            self.send_response(200)
            # response header:
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            # response body:
            self.wfile.write(bytes(json.dumps(oneMovie), "utf-8")) # jsonify
        else:
            self.handleNotFound()

    def handleDeleteMovie(self, movie_id):
        db = MoviesDB()
        oneMovie = db.getOneMovie(movie_id)

        if oneMovie != None:
            db.deleteMovie(movie_id)
            # response status code:
            self.send_response(200)
            # response header:
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            self.handleNotFound()

    def handleCreateMovie(self):
        print("request headers:", self.headers)

        # 1. read the data in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body:", parsed_body)

        # 2. save movie name to the "database"
        movie_name = parsed_body["name"][0] # index the dictionary & list
        movie_rating = parsed_body["rating"][0] # index the dictionary & list
        movie_genre = parsed_body["genre"][0] # index the dictionary & list
        db = MoviesDB()
        db.createMovie(movie_name, movie_rating, movie_genre)

        # 3. send a response
        self.send_response(201)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        self.loadSession()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.loadSession()
        path_parts = self.path.split("/")
        if len(path_parts) == 3:
            collection_name = path_parts[1]
            member_id = path_parts[2]
        else:
            collection_name = path_parts[1]
            member_id = None

        if collection_name == "movies":
            if member_id:
                self.handleGetMoviesMember(member_id)
            else:
                self.handleGetMoviesCollection()
        else:
            self.handleNotFound()

    def do_POST(self):
        self.loadSession()
        if self.path == "/movies":
            self.handleCreateMovie()
        else:
            self.handleNotFound()

    def do_DELETE(self):
        self.loadSession()
        path_parts = self.path.split("/")
        if len(path_parts) == 3:
            collection_name = path_parts[1]
            member_id = path_parts[2]
        else:
            collection_name = path_parts[1]
            member_id = None

        if collection_name == "movies":
            if member_id:
                self.handleDeleteMovie(member_id)
            else:
                self.handleNotFound()
        else:
            self.handleNotFound()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run():
    listen = ("127.0.0.1", 8080)
    server = ThreadedHTTPServer(listen, MyRequestHandler)

    print("Server running!")
    server.serve_forever()

if __name__ == '__main__':
    run()
