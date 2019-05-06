import sqlite3
from hashlib import md5


class DbCommunicator:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def get_dims(self, image: bytearray):
        return(0,0)

    def add(self, image: bytearray):
        db = sqlite3.connect(self.db_name)
        width, height = self.get_dims(image)
        name = md5(image).hexdigest()
        color = get_color(image)
        db.execute("insert into Imagens values (?, ?, ?, ?);", (name, height, width, color,))
