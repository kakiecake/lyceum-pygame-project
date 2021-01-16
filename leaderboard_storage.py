from score import Score
from typing import List
import sqlite3


class LeaderboardStorage:
    def __init__(self, connection: sqlite3.Connection):
        self._cursor: sqlite3.Cursor = connection.cursor()
        self._connection = connection

    def add_new_score(self, username: str, score: int, level: str):
        sql = 'insert into scores(username, score, level) values (?, ?, ?)'
        data = (username, score, level)
        self._cursor.execute(sql, data)
        self._connection.commit()

    def get_user_highscore(self, username: str, level: str) -> int:
        sql = 'select max(score) from scores where username = ? ' +\
            'and level = ? sort by score'
        data = (username, level)
        query_result = self._cursor.execute(sql, data)
        return query_result

    def get_all_level_scores(self, level: str) -> List[Score]:
        sql = 'select username, score, level from scores where level = ? order by score desc'
        data = (level,)
        query_result = self._cursor.execute(sql, data)
        return [Score(*x) for x in query_result]

    def get_unique_level_scores(self, level: str) -> List[Score]:
        sql = 'select username, max(score), level from scores ' +\
            'where level = ? group by username order by score desc'
        data = (level,)
        query_result = self._cursor.execute(sql, data)
        return [Score(*x) for x in query_result]
