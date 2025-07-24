import sqlite3
from datetime import datetime

class habit_db:

    def __init__(self):
        """creates/connects to a database."""
        self.conn = sqlite3.connect("Habits.db")
        self.cursor = self.conn.cursor()
        self.habits_table()
        self.streak_counter()

    def habits_table(self):
        '''create the habits table.'''
        #creates and connects to a habits database if it doesn't exists.
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS habits(
            name TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            date_created TEXT DEFAULT (date('now')),
            current_streak INTEGER DEFAULT 0,
            streak_since TEXT DEFAULT (date('now')),
            longest_streak INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Incomplete',
            last_updated TEXT NULL)"""
        )
        self.conn.commit()

    def close_connection(self):
        """closes the connection."""
        self.conn.close()

    def examples(self):
        """loads example habits if not loaded."""
        examples = [
            #name, periodicity, date_created, current_streak, streak_since, longest_streak, status, last_updated.
            #PS: periodicity and status start with capital a letter, date format is %Y-%m-%d.
            ('h1', 'Daily', '2024-12-31', 3, '2025-06-10', 51, 'Incomplete', '2025-06-13'),
            ('h2', 'Weekly', '2024-12-31', 3, '2025-06-10', 51, 'Incomplete', '2025-06-13'),
            ('h3', 'Daily', '2024-12-31', 3, '2025-06-10', 51, 'Incomplete', '2025-06-13'),
            ('h4', 'Weekly', '2024-12-31', 3, '2025-06-10', 51, 'Incomplete', '2025-06-13'),
            ('h5', 'Daily', '2024-12-31', 3, '2025-06-10', 51, 'Incomplete', '2025-06-13')
        ]

        try:
            #checks if the habit already exists before adding it.
            for eg in examples:
                self.cursor.execute(
                    """INSERT OR IGNORE INTO habits
                    (name, periodicity, date_created, current_streak, streak_since, longest_streak, status, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", eg
                )
            
            self.conn.commit()
        except Exception as e:
            print(f"{e} error occurred.")

    def add_habit(self, name, periodicity):
        """adds a habit."""
        try:
            self.cursor.execute("SELECT * FROM habits WHERE name = ?", (name,))
            loaded = self.cursor.fetchone()

            #check if the habit already exists.
            if loaded:
                print("Habit already exists.")
            else:
                self.cursor.execute(
                    """INSERT INTO habits (name, periodicity) VALUES (?,?)""",
                    (name, periodicity)
                )
                self.conn.commit()
                print("Habit added successfully.")
        except Exception as e:
            print(f"{e} error occurred.")

    def print_habits(self, category):
        """prints all habits or habits of a certain periodicity."""
        try:
            if category == 'Weekly':
                self.cursor.execute("SELECT name, periodicity, current_streak, status, date_created FROM habits WHERE periodicity = 'Weekly'")
            elif category == 'Daily':
                self.cursor.execute("SELECT name, periodicity, current_streak, status, date_created FROM habits WHERE periodicity = 'Daily'")
            else:
                self.cursor.execute("SELECT name, periodicity, current_streak, status, date_created FROM habits")

            habits = self.cursor.fetchall()
            self.conn.commit()

            #shows what each value means.
            print('name---periodicity---current streak---status---date created')

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
            #fetches the habit
            self.cursor.execute(
                """SELECT COUNT(*) FROM habits 
                WHERE name = ? AND 
                status = 'Incomplete' AND
                (date(last_updated) < date('now') OR last_updated IS NULL)""",
                (name,)
            )
            print(f"Matching rows before update: {self.cursor.fetchone()[0]}")
            
            #Updates the status, streak and last updated columns
            self.cursor.execute(
                """UPDATE habits 
                SET status = 'Complete',
                current_streak = current_streak + 1,
                last_updated = date('now')
                WHERE name = ? AND 
                (date(last_updated) < date('now') OR last_updated IS NULL)""",
                (name,)
            )

            #Updates the longest streak if current streak is higher.
            self.cursor.execute(
                """UPDATE habits
                SET longest_streak = current_streak
                WHERE name = ? AND
                current_streak > longest_streak""",
                (name,)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"{e} error occurred.")
        except Exception as e:
            print(f"{e} error occurred.")     
    
    def streak_counter(self):
        """resets current streak if broken and habit status."""
        try: 
            #fetches daily habits
            self.cursor.execute(
                """SELECT name, current_streak, last_updated,
                COALESCE(julianday(last_updated) - julianday(streak_since), 0) AS day_diff,
                COALESCE(julianday('now') - julianday(last_updated), 0) AS update_diff
                FROM habits WHERE periodicity = 'Daily'"""
            )   
            daily_habits = self.cursor.fetchall()

            for habit in daily_habits:
                #Checks if at least a day has passed since last update to reset status.
                if habit[4] >= 1:
                    self.cursor.execute("UPDATE habits SET status = 'Incomplete' WHERE name = ?", (habit[0],))

                    #Checks if streak is broken or not.
                    if habit[1] <= habit[3] or habit[3] is None:
                        self.cursor.execute("UPDATE habits SET current_streak = 0 WHERE name = ?", (habit[0],))

            #Fetches weekly habits.
            self.cursor.execute(
                """SELECT name, current_streak, last_updated,
                COALESCE(julianday(last_updated) - julianday(streak_since), 0) AS day_diff,
                COALESCE(julianday('now') - julianday(streak_since), 0) AS update_diff
                FROM habits WHERE periodicity = 'Weekly'"""
            )   
            weekly_habits = self.cursor.fetchall()

            for habit in weekly_habits:
                weeks = habit[3]/7
                days_left = habit[3]//7

                #Checks if a streak number matches the number of weeks since streak started.
                if habit[4] >= 7:
                    self.cursor.execute("UPDATE habits SET status = 'Incomplete' WHERE name = ?", (habit[0],))

                    #Checks if more than a week passed since last update to reset streak.
                    if habit[4] % 7 > habit[1] or habit[3] is None:
                        self.cursor.execute("UPDATE habits SET current_streak = 0 WHERE name = ?", (habit[0],))
  
            self.conn.commit()

        except Exception as e:
            print(f"{e} error occurred.")

    def delete_all(self):
        """deletes all habits."""
        try:
            self.cursor.execute("""DELETE FROM habits""")
            self.conn.commit()
        except Exception as e:
            print(f"{e} error occurred.")
