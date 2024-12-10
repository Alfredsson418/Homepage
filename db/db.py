import sqlite3
from os import path
import logs.log as log
from dataclasses import dataclass

@dataclass
class project:
    id: int
    name: str
    url: str

class db:
    conn: sqlite3.Connection

    def __init__(self, file_path):
        self.path = path.abspath(file_path)
        log.logging.info("Database init")


    def __open(self):
        self.conn = sqlite3.connect(self.path)
    def __close(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.__open()

        self.conn.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
                name TEXT NOT NULL,
                url TEXT
            )
            """
        )

        self.__close()

    def set_new(self, data):
        self.__open()
        if (isinstance(data, project)):
            self.conn.execute(
                "INSERT INTO projects (name, url) VALUES (?, ?)",
                (data.name, data.url)
            )
        else:
            log.logging.critical("Failed to add to database")

        self.__close()

    def update(self, data):
        self.__open()
        if (isinstance(data, project)):
            self.conn.execute(
                "UPDATE projects SET name = ?, url = ? WHERE ID = ?",
                (data.name, data.url, data.id)
            )
        else:
            log.logging.critical("Failed to update database")

        self.__close()

    def get_table(self, type):
        self.__open()

        cursor = self.conn.cursor()

        tubles = []

        if (isinstance(type, project)):
            cursor.execute(
                "SELECT * FROM project"
            )
            tubles = cursor.fetchall()
        else:
            log.logging.critical("Failed to fetch from databases")


        self.__close()

        return tubles
