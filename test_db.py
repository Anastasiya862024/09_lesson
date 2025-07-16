import pytest
from sqlalchemy import create_engine, text

db = create_engine("postgresql://postgres:Styura86@localhost:5432/QA")


@pytest.fixture(scope='function')
def connection():
    conn = db.connect()
    yield conn
    conn.commit()
    conn.close()


def test_add_new(connection):
    sql = text("INSERT INTO student (user_id, level, education_form,\
               subject_id) VALUES (:u_id, :lev, :e_form, :s_id)")
    connection.execute(sql, {"u_id": 99999, "lev": 'Pre-Intermediate', "e_form": 'group', "s_id": 1})

    result = connection.execute(
        text("SELECT level FROM student WHERE user_id = 99999"))
    title = result.fetchone()
    assert title[0] == "Pre-Intermediate"


def test_update(connection):
    sql = text("UPDATE student SET level = :lev WHERE user_id = :u_id")
    connection.execute(sql, {"lev": "Beginner", "u_id": 99999})

    result = connection.execute(
        text("SELECT level FROM student WHERE user_id = 99999"))
    title = result.fetchone()
    assert title[0] == "Beginner"


def test_delete(connection):
    sql = text("DELETE FROM student WHERE user_id = :u_id")
    connection.execute(sql, {"u_id": 99999})

    result = connection.execute(
        text("SELECT level FROM student WHERE user_id = 99999"))
    title = result.fetchone()
    assert title is None
