# habit-app

## Overview

The Habit Tracker is a Python-based backend application designed to help users manage and track their habits efficiently. Utilizing the `questionary` library for a user-friendly command-line interface and `sqlite3` for a lightweight database, this app streamlines the habit tracking process.

## Features

- **Interactive CLI**: Provides a smooth user experience through the `questionary` library.
- **Persistent Data**: Uses `sqlite3` for storing and retrieving habit information, ensuring data is retained between sessions.
- **Easy Habit Management**: Create, read, update, and delete habits effortlessly.


## Installation

First clone the repository using 

```bash
https://github.com/Mosayab/habit-app
```

Then install the requirements using

```bash
pip install -r requirements.txt
```

## main.py

Uses questionary as the UI in the terminal.

Loops through the code with a while loop until it is closed.

Displays the functions the app can run.

## habit_db.py

Has two database tables, habits and logs, to store information.

Contains all function codes.

## habits table

Stores habit name, periodicity, status, streak, longest streak and date created.
<img width="1084" height="243" alt="Screenshot 2026-02-10 213606" src="https://github.com/user-attachments/assets/07011015-743c-44d2-9256-75ab977c9a60" />

## logs table

Stores habit completion dates and streak
<img width="768" height="76" alt="image" src="https://github.com/user-attachments/assets/625c8199-0c61-46b4-999a-447c9872c60b" />
<img width="805" height="130" alt="Screenshot 2026-02-10 213628" src="https://github.com/user-attachments/assets/4482c38c-a9a8-41fc-b292-e7e335a0339b" />

## pictures of the app

all functions
<img width="435" height="262" alt="Screenshot 2026-02-27 131452" src="https://github.com/user-attachments/assets/efdc563e-79d5-4cc6-9bc8-369d10b7ab1a" />

adding a habit
<img width="406" height="133" alt="Screenshot 2026-02-27 131556" src="https://github.com/user-attachments/assets/855638d4-26b4-46f9-92eb-f98bd3cca12f" />
<img width="392" height="86" alt="Screenshot 2026-02-27 131616" src="https://github.com/user-attachments/assets/e2196da6-e55e-493e-8e84-ea5a1b252abf" />

completing a habit
<img width="445" height="193" alt="Screenshot 2026-02-27 131627" src="https://github.com/user-attachments/assets/7f9a24e3-c1ef-4d23-8b2e-a6ec15435a8d" />

deleting a habit
<img width="405" height="209" alt="Screenshot 2026-02-27 131648" src="https://github.com/user-attachments/assets/8d54e063-3157-46cf-84d4-7e1d71dabc39" />

viewing habits
<img width="449" height="157" alt="Screenshot 2026-02-27 131749" src="https://github.com/user-attachments/assets/78b1a553-779d-498a-afdd-65de7cb8bc11" />
<img width="429" height="134" alt="Screenshot 2026-02-27 131716" src="https://github.com/user-attachments/assets/1f07688e-7bc2-4f59-b694-ac11ef548482" />
<img width="448" height="92" alt="Screenshot 2026-02-27 131736" src="https://github.com/user-attachments/assets/dc7eef51-c86f-4223-bb1e-e461e03f72a9" />

viewing longest streak of a habit
<img width="581" height="204" alt="Screenshot 2026-02-27 131835" src="https://github.com/user-attachments/assets/8612c716-b588-492f-8a5f-c61cbc0c38ba" />

viewing longeset streak of all habits
<img width="585" height="135" alt="Screenshot 2026-02-27 131851" src="https://github.com/user-attachments/assets/cc6b5536-edef-41a6-8f60-edb9f906a9b9" />

trying to load the examples multiple times
<img width="421" height="53" alt="Screenshot 2026-02-27 131924" src="https://github.com/user-attachments/assets/d71f4082-e508-4767-8c81-5ab716ae4e07" />

checking a habit's stats
<img width="450" height="399" alt="Screenshot 2026-02-27 131947" src="https://github.com/user-attachments/assets/bea59ae9-2aed-4ce0-8c8b-884f2b81a950" />
