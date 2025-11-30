import sqlite3
import random
from datetime import datetime, timedelta

class habit_db:

    def __init__(self, db_path="Habits.db"):
        """creates/connects to a database."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.habits_table()
        self.logs_table()

    def habits_table(self):
        '''create the habits table.'''
        #creates and connects to a habits database if it doesn't exists.
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS habits(
            name TEXT NOT NULL PRIMARY KEY,
            periodicity TEXT NOT NULL,
            date_created TEXT DEFAULT (date('now')),
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Incomplete'
            )"""
        )
        self.conn.commit()

    def logs_table(self):
        '''create the logs table.'''
        #creates and connects to a logs database if it doesn't exists.
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            date TEXT DEFAULT (date('now')),
            status TEXT NOT NULL,
            streak INTEGER DEFAULT 0,
            FOREIGN KEY (habit_name) REFERENCES habits(name)
            )"""
        )
        self.conn.commit()

    def close_connection(self):
        """closes the connection."""
        self.conn.close()

    def examples(self):
        """loads example habits if not loaded with 4 weeks of predefined data."""
        examples = [
            ('h1', 'Daily'),
            ('h2', 'Weekly'),
            ('h3', 'Daily'),
            ('h4', 'Weekly'),
            ('h5', 'Daily')
        ]

        try:
            #makes sure examples aren't already loaded
            self.cursor.execute("SELECT * FROM habits WHERE name = 'h1'")
            loaded = self.cursor.fetchone()

            if loaded:
                print("Examples already loaded.")
                return
            
            today = datetime.now().date()
            start_date = today - timedelta(days=27)

            #checks if the habit already exists before adding it.
            for name, periodicity in examples:
                self.cursor.execute(
                    """INSERT OR IGNORE INTO habits (name, periodicity, date_created) VALUES (?, ?, ?)""",
                    (name, periodicity, start_date.isoformat())
                )

            for name, periodicity in examples:
                current_date = start_date
                streak = 0

                while current_date <= today:
                    insert_event = False

                    if periodicity.lower() == "daily":
                        insert_event = True
                    elif periodicity.lower() == "weekly" and current_date.weekday() == 0:
                        insert_event = True

                    if insert_event:
                        completed = random.random() < 0.8
                        status = "Completed" if completed else "Incomplete"

                        # streak maths
                        if completed:
                            streak += 1
                        else:
                            streak = 0

                        self.cursor.execute(
                            """INSERT OR IGNORE INTO logs (habit_name, date, status, streak) VALUES (?, ?, ?, ?)""",
                            (name, current_date.isoformat(), status, streak)
                            )
                        
                    current_date += timedelta(days=1)
                    
                    self.cursor.execute(
                        """ SELECT streak FROM logs
                        WHERE habit_name = ?
                        ORDER BY date DESC LIMIT 1""",
                        (name,)
                    )
                    log = self.cursor.fetchone()
                    current_streak = log[0] if log else 0

                    self.cursor.execute(
                        """SELECT MAX(streak) FROM logs WHERE habit_name = ?""",
                        (name,)
                    )
                    longest_streak = self.cursor.fetchone()[0] or 0

                    self.cursor.execute(
                        """UPDATE habits
                        SET current_streak = ?, longest_streak = ?, status = 'Incomplete' WHERE name = ?""",
                        (current_streak, longest_streak, name)
                    )
            
            self.conn.commit()
        except Exception as e:
            print(f"{e} error occurred.")

    def add_habit(self, name, periodicity):
        """adds a habit."""
        try:
            self.cursor.execute("SELECT * FROM habits WHERE name = ?", (name,))
            loaded = self.cursor.fetchone()

            #check if habit already exists
            if loaded:
                print("Habit already exists.")
                return
            else:
                self.cursor.execute(
                    """INSERT INTO habits (name, periodicity) VALUES (?,?)""",
                    (name, periodicity)
                )
                self.cursor.execute(
                    """INSERT INTO logs (habit_name, date, status, streak) VALUES (?, date('now'), 'Incomplete', 0)""",
                    (name,)
                )
                self.conn.commit()
                print("Habit added successfully.")
        except Exception as e:
            print(f"{e} error occurred.")

    def print_habits(self, category):
        """prints all habits or habits of a certain periodicity."""
        try:
            if category == 'Weekly':
                self.cursor.execute("SELECT name, periodicity, current_streak, status FROM habits WHERE periodicity = 'Weekly'")
            elif category == 'Daily':
                self.cursor.execute("SELECT name, periodicity, current_streak, status FROM habits WHERE periodicity = 'Daily'")
            else:
                self.cursor.execute("SELECT name, periodicity, current_streak, status FROM habits")

            habits = self.cursor.fetchall()
            self.conn.commit()

            #shows what each value means.
            print('name---periodicity---current streak---status')

            for x in habits:
                print(x)
        except Exception as e:
            print(f"{e} error occurred.")

    def longest_streak(self, name):
        """prints a habit name and its longest streak."""
        try:
            self.cursor.execute("SELECT name, longest_streak FROM habits WHERE name = ?", (name,))
            loaded = self.cursor.fetchone()

            #check if habit exists
            if loaded:
                print(loaded)
            else:
                print("Habit not found")

            self.conn.commit()
        except Exception as e:
            print(f"{e} error occurred.")

    def all_longest_streaks(self):
        """prints all habit names and their longest streak."""
        try:
            self.cursor.execute("SELECT name, longest_streak FROM habits")
            for row in self.cursor.fetchall():
                print(row)
            self.conn.commit()
        except Exception as e:
            print(f"{e} error occurred.")

    def incomplete_habits(self):
        """prints incomplete habits."""
        try:
            #fetches incomplete habits
            self.cursor.execute("SELECT name FROM habits WHERE status = 'Incomplete'")
            
            for x in self.cursor.fetchall():
                print(x)
            
            self.conn.commit()
        except Exception as e:
            print(f"{e} error occurred.")

    def complete_habit(self, name):
        """marks a habit as complete."""
        try:
            #checks if the habit exists
            self.cursor.execute(
                """SELECT * FROM habits WHERE name = ?""",
                (name,)
            )
            loaded = self.cursor.fetchone()

            if loaded:
                #Updates habit status
                streak = loaded[3]+1
                longest_streak = loaded[4]

                if streak > longest_streak:
                    longest_streak = streak

                self.cursor.execute(
                    """UPDATE habits SET status = 'Completed', current_streak = ?, longest_streak = ?  WHERE name = ?""",
                    (streak, longest_streak, name)
                )
            else:
                print("Habit not found.")
                return
             
            #fetch latest habit logs
            self.cursor.execute(
                """SELECT streak, status FROM logs
                WHERE habit_name = ?
                ORDER BY date DESC LIMIT 1""",
                (name,)
            )
            latest_log = self.cursor.fetchone()

            #streak math
            if latest_log and latest_log[1] == 'completed':
                current_streak = latest_log[0] + 1
            else:
                current_streak = 1

            #Updates logs 
            self.cursor.execute(
                """INSERT INTO logs (habit_name, date, status, streak) VALUES (?, date('now'), 'Completed', ?)""",
                (name, current_streak)
            )

            self.conn.commit()

        except sqlite3.Error as e:
            print(f"{e} error occurred.")
            
        except Exception as e:
            print(f"{e} error occurred.")     
    
    def habit_stats(self, name):
        """prints statistics for a specific habit."""
        try:
            self.cursor.execute(
                """SELECT name, periodicity, current_streak, longest_streak, date_created FROM habits WHERE name = ?""",
                (name,)
            )
            habit = self.cursor.fetchone()

            if habit:
                print(f"Habit Stats for {name}:")
                print(f"Periodicity: {habit[1]}")
                print(f"Current Streak: {habit[2]}")
                print(f"Longest Streak: {habit[3]}")
                print(f"Date Created: {habit[4]}")
            else:
                print("Habit not found.")

            self.conn.commit()
        except Exception as e:
            print(f"{e} error occurred.")

    def habit_logs(self, name):
        """prints logs for a specific habit."""
        try:
            self.cursor.execute(
                """SELECT date, status, streak FROM logs WHERE habit_name = ? ORDER BY date""",
                (name,)
            )
            logs = self.cursor.fetchall()

            if logs:
                print(f"Logs for {name}:")
                for log in logs:
                    print(f"Date: {log[0]}, Status: {log[1]}, Streak: {log[2]}")
            else:
                print("No logs found for this habit.")

            self.conn.commit()
        except Exception as e:
            print(f"{e} error occurred.")

    def delete_all(self):
        """deletes all habits."""
        try:
            self.cursor.execute("""DELETE FROM logs""")
            self.cursor.execute("""DELETE FROM habits""")
            self.conn.commit()
        except Exception as e:
            print(f"{e} error occurred.")