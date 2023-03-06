import sqlite3

# first, use sqlite3 in terminal to create a database and table:
# CREATE TABLE movies (id INTEGER PRIMARY KEY, name TEXT, rating INTEGER, genre TEXT);

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class MoviesDB:

    def __init__(self):
        self.connection = sqlite3.connect("movies_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def createMovie(self, name, rating, genre):
        # INSERT record into table
        data = [name, rating, genre]
        self.cursor.execute("INSERT INTO movies (name, rating, genre) VALUES (?, ?, ?)", data)
        self.connection.commit()

    # returns a list of dictionaries (or an empty list if there are no records)
    def getAllMovies(self):
        # read all records from table
        self.cursor.execute("SELECT * FROM movies")
        records = self.cursor.fetchall()
        return records

    # returns a single dictionary (or None if the movie_id does not exist)
    def getOneMovie(self, movie_id):
        data = [movie_id]
        self.cursor.execute("SELECT * FROM movies WHERE id = ?", data)
        record = self.cursor.fetchone()
        return record


# DELETE FROM movies WHERE id = ?

# UPDATE movies SET name = ?, rating = ?, genre = ? WHERE id = ?
