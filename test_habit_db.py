import pytest
from habit_db import habit_db

@pytest.fixture

def db():
    #A habit database for testing
    test_db = habit_db(":memory:")
    test_db.cursor.execute("PRAGMA foreign_keys = ON;")
    yield test_db
    #Teardown: close connection
    test_db.close_connection()

def test_add_habit(db):
    #Test for daily habits
    db.add_habit("Test1", "Daily")
    db.cursor.execute("SELECT name, periodicity FROM habits WHERE name = ?", ("Test1",))
    habit = db.cursor.fetchone()
    assert habit == ("Test1", "Daily")
    db.cursor.execute("SELECT status, streak FROM logs WHERE habit_name = ? ORDER BY id DESC LIMIT 1", ("Test1",))
    logs = db.cursor.fetchone()
    assert logs == ("Incomplete", 0)

    #Test for weekly habits
    db.add_habit("Test2", "Weekly")
    db.cursor.execute("SELECT name, periodicity FROM habits WHERE name = ?", ("Test2",))
    habit = db.cursor.fetchone()
    assert habit == ("Test2", "Weekly")
    db.cursor.execute("SELECT status, streak FROM logs WHERE habit_name = ? ORDER BY id DESC LIMIT 1", ("Test2",))
    logs = db.cursor.fetchone()
    assert logs == ("Incomplete", 0)

def test_add_duplicate_habit(db, capsys):
    #Test for duplicate habits
    db.add_habit("Test1", "Daily")
    db.add_habit("Test1", "Daily")
    output = capsys.readouterr()
    assert "Habit already exists." in output.out

def test_complete_habit(db):
    #Test for completing a habit
    db.add_habit("Test1", "Daily")
    db.complete_habit("Test1")
    db.cursor.execute("SELECT status, current_streak FROM habits WHERE name = ?", ("Test1",))
    habit = db.cursor.fetchone()
    assert habit == ("Completed", 1)
    db.cursor.execute("SELECT status, streak FROM logs WHERE habit_name = ? ORDER BY id DESC LIMIT 1", ("Test1",))
    logs = db.cursor.fetchone()
    assert logs == ("Completed", 1)

def test_delete_all(db):
    #Test for deleting all habits
    db.add_habit("Test1", "Daily")
    db.add_habit("Test2", "Daily")
    db.delete_all()
    db.cursor.execute("SELECT * FROM habits")
    habits = db.cursor.fetchall()
    assert habits == []