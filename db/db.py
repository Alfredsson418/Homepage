import sqlite3
from os import path
import logs.log as log
from dataclasses import dataclass

@dataclass
class project_class:
    id: str = ""
    id_old: str = ""
    name: str = ""
    url: str = ""
    color: str = ""
    descr: str = ""

@dataclass
class blog_class:
    id: str = ""
    title: str = ""
    text: str = ""


class db:
    conn: sqlite3.Connection

    def __init__(self, file_path):
        self.path = path.abspath(file_path)
        self.create_table()
        log.logging.info("Database init")

    def __open(self):
        try:
            self.conn = sqlite3.connect(self.path)
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            log.logging.critical(f"Failed to open database: {e}")

    def __close(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.__open()

        self.conn.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                url TEXT,
                descr TEXT,
                color TEXT NOT NULL
            )
            """
        )

        self.conn.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS blog_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                text TEXT NOT NULL
            )
            """
        )

        self.__close()

    def set_new(self, data):
        try:
            self.__open()
            if (isinstance(data, project_class)):
                self.conn.execute(
                    "INSERT INTO projects (name, url, color, descr) VALUES (?, ?, ?, ?)",
                    (data.name, data.url, data.color, data.descr,)
                )
            elif (isinstance(data, blog_class)):
                self.conn.execute(
                    "INSERT INTO blog_posts (title, text) VALUES (?, ?)",
                    (data.title, data.text,)
                )
            else:
                log.logging.critical(f"Datatype is not supported {data}")
        except Exception as e:
            log.logging.critical(f"Failed to insert into database: {e}")
        finally:
            self.__close()

    def update(self, data):
        try:
            self.__open()
            if (isinstance(data, project_class)):
                self.conn.execute(
                    "UPDATE projects SET id = ?, name = ?, url = ?, color = ?, descr = ? WHERE id = ?",
                    (data.id, data.name, data.url, data.color, data.descr, data.id_old,)
                )
            elif (isinstance(data, blog_class)):
                self.conn.execute(
                    "UPDATE blog_posts SET title = ?, text = ? WHERE id = ?",
                    (data.title, data.text, data.id,)
                )
            else:
                log.logging.critical(f"Datatype is not supported {data}")
        except Exception as e:
            log.logging.critical(f"Failed to update database: {e}")
        finally:
            self.__close()

    def delete(self, data):
        try:
            self.__open()
            if (isinstance(data, project_class)):
                self.conn.execute(
                    "DELETE FROM projects WHERE ID = ?",
                    (data.id,)
                )
            elif (isinstance(data, blog_class)):
                self.conn.execute(
                    "DELETE FROM blog_posts WHERE ID = ?",
                    (data.id,)
                )
            else:
                log.logging.critical(f"Datatype is not supported {data}")
        except Exception as e:
            log.logging.critical(f"Failed to delete from database: {e}")
        finally:
            self.__close()

    def get_table(self, type):
        tuples = None
        try:
            self.__open()

            if(isinstance(type, project_class)):
                tuples = self.conn.execute(
                    "SELECT * FROM projects"
                ).fetchall()
            elif (isinstance(type, blog_class)):
                tuples = tuples = self.conn.execute(
                    "SELECT * FROM blog_posts"
                ).fetchall()
            else:
                log.logging.critical(f"Datatype is not supported {type}")
        except Exception as e:
            log.logging.critical(f"Failed to get from database: {e}")
        finally:
            self.__close()

        return tuples
