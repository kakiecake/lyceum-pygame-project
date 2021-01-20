import sqlite3
import hashlib


class UserStorage:
    def __init__(self, connection: sqlite3.Connection):
        self._cursor: sqlite3.Cursor = connection.cursor()
        self._connection = connection

    def register_user(self, username: str, password: str) -> bool:
        try:
            sql = 'insert into users(username, password_hash) values (?, ?)'
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            data = (username, password_hash)
            self._cursor.execute(sql, data)
            self._connection.commit()
        except sqlite3.IntegrityError:
            return False
        else:
            return True

    def login_user(self, username: str, password: str) -> bool:
        sql = 'select username from users where username = ? and password_hash = ?'
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        data = (username, password_hash)
        result = self._cursor.execute(sql, data).fetchone()
        return bool(result)
