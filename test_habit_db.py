import pytest
from habit_db import habit_db

@pytest.fixture
def db():
    """A habit database for testing"""
    test_db = habit_db(":memory:")
    test_db.cursor.execute("PRAGMA foreign_keys = ON;")
    yield test_db

    #Teardown: close connection
    test_db.close_connection()

def test_add_habit(db):
    """Test for adding habits"""
    #adding a daily habit
    db.add_habit("Test1", "Daily")
    db.cursor.execute("SELECT name, periodicity FROM habits WHERE name = ?", ("Test1",))
    habit = db.cursor.fetchone()
    assert habit == ("Test1", "Daily")
    db.cursor.execute("SELECT status, streak FROM logs WHERE habit_name = ? ORDER BY id DESC LIMIT 1", ("Test1",))
    logs = db.cursor.fetchone()
    assert logs == ("Incomplete", 0)

    #adding a weekly habits
    db.add_habit("Test2", "Weekly")
    db.cursor.execute("SELECT name, periodicity FROM habits WHERE name = ?", ("Test2",))
    habit = db.cursor.fetchone()
    assert habit == ("Test2", "Weekly")
    db.cursor.execute("SELECT status, streak FROM logs WHERE habit_name = ? ORDER BY id DESC LIMIT 1", ("Test2",))
    logs = db.cursor.fetchone()
    assert logs == ("Incomplete", 0)

def test_add_duplicate_habit(db, capsys):
    """Test for duplicate habits"""
    db.add_habit("Test1", "Daily")
    db.add_habit("Test1", "Daily")
    output = capsys.readouterr()
    assert "Habit already exists." in output.out

def test_complete_habit(db):
    """test to complete a habit"""
    db.add_habit("Test1", "Daily")
    db.complete_habit("Test1")

    #checking habits table
    db.cursor.execute("SELECT status, current_streak FROM habits WHERE name = ?", ("Test1",))
    habit = db.cursor.fetchone()
    assert habit == ("Completed", 1)

    #checking logs table
    db.cursor.execute("SELECT status, streak FROM logs WHERE habit_name = ? ORDER BY id DESC LIMIT 1", ("Test1",))
    logs = db.cursor.fetchone()
    assert logs == ("Completed", 1)

def test_delete_all(db):
    """test to delete all habits"""
    db.add_habit("Test1", "Daily")
    db.add_habit("Test2", "Daily")
    db.delete_all()

    #checking habits table
    db.cursor.execute("SELECT * FROM habits")
    habits = db.cursor.fetchall()
    assert habits == []

    #checking logs table
    db.cursor.execute("SELECT * FROM logs")
    logs = db.cursor.fetchall()
    assert logs == []

def test_examples(db):
    """test for loading examples"""
    db.examples()
    db.cursor.execute("SELECT name FROM habits")
    habits = db.cursor.fetchall()
    assert habits == [('h1',), ('h2',), ('h3',), ('h4',), ('h5',)]

def test_print_habits(db, capsys):
    """test for printing habits"""
    db.add_habit("test1", "Daily")
    db.add_habit("test2", "Weekly")

    #daily habits
    db.print_habits("Daily")
    output = capsys.readouterr()
    assert "test1" in output.out
    assert "('test2',)" not in output.out

    #weekly habits
    db.print_habits("Weekly")
    output = capsys.readouterr()
    assert "test2" in output.out
    assert "('test1',)" not in output.out

    #all habits
    db.print_habits("All")
    output = capsys.readouterr()
    assert "test1" in output.out
    assert "test2" in output.out

def test_longest_streak(db, capsys):
    """test for printing longest streak for a habit"""
    db.add_habit("test1", "Daily")
    db.longest_streak("test1")
    output = capsys.readouterr()
    assert "('test1', 0)" in output.out

def test_all_longest_streaks(db, capsys):
    """test for printing longest streak for all habits"""
    db.add_habit("test1", "Daily")
    db.add_habit("test2", "Daily")
    db.all_longest_streaks()
    output = capsys.readouterr()
    assert "('test1', 0)" in output.out
    assert "('test2', 0)" in output.out

def test_incomplete_habits(db, capsys):
    """test for printing incomplete habits"""
    db.add_habit("test1", "Daily")
    db.add_habit("test2", "Daily")
    db.complete_habit("test1")
    db.incomplete_habits()
    output = capsys.readouterr()
    assert "('test1',)" not in output.out
    assert "('test2',)" in output.out

def test_habit_stats(db, capsys):
    """test for checking habit stats"""
    db.add_habit("test1", "Daily")
    db.habit_stats("test1")
    output = capsys.readouterr()

    assert "Habit Stats for test1:" in output.out
    assert "Periodicity: Daily" in output.out
    assert "Current Streak:" in output.out
    assert "Longest Streak:" in output.out
    assert "Date Created:" in output.out

def test_habit_logs(db, capsys):
    """test for habit logs"""
    db.add_habit("test1", "Daily")
    db.habit_logs("test1")
    output = capsys.readouterr()
    assert "Status: Incomplete, Streak: 0" in output.out

    db.complete_habit("test1")
    db.habit_logs("test1")
    output = capsys.readouterr()
    assert "Status: Completed, Streak: 1" in output.out

def test_delete_habit(db, capsys):
    """test for deleting a habit"""
    db.add_habit("test1", "Daily")
    db.add_habit("test2", "Weekly")

    db.delete_habit("test1")
    db.print_habits("All")
    output = capsys.readouterr()
    assert "test1" not in output.out

def test_habit_names(db, capsys):
    """test for printing habit names"""
    db.add_habit("test1", "Daily")
    db.add_habit("test2", "Daily")
    db.habit_names()

    output = capsys.readouterr()
    assert "test1" in output.out
    assert "test2" in output.out