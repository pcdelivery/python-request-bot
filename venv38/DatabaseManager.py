import sqlite3
from venv38.Models.UserRequest import UserRequest
from typing import Dict, List, Tuple

conn = sqlite3.connect("data/new_data.db")
cursor = conn.cursor()

REQUEST_QUE_TABLE = "requests_questions"
REQUEST_ANS_TABLE = "requests_answers"


def _init_():
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def req_insert(request: UserRequest):
    for que in request.questions:
        cursor.execute(
            f"INSERT INTO {REQUEST_QUE_TABLE}" +
            "(title, size)" +
            f"VALUES ({que.question}, {que.size})"
        )

        for ans in que.answers:
            cursor.execute(
                f"INSERT INTO {REQUEST_ANS_TABLE}" +
                "(text, is_true)" +
                f"VALUES ({ans.answer_text}, {ans.is_true})"
            )


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result