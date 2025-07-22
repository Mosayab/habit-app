import questionary
from habit_db import habit_db

start = questionary.confirm("Would you like to open the app?").ask()

hdb = habit_db()

while start == True:
  
  task = questionary.select(
    "What would you like to do?",
    choices=[
      "Add a habit",
      "Complete habit",
      "Delete all habits",
      "View habit list",
      "View longest streak of a habit",
      "View longest streak of all habits",
      "Load examples",
      "Close app"
    ]
  ).ask()

  match task:

    case "Add a habit":
      name = questionary.text("Habit name: ").ask()
      periodicity = questionary.select(
        "Periodicity: ",
        choices = [
          "Daily",
          "Weekly"
        ]
      ).ask()

      hdb.add_habit(name, periodicity)

    case "Complete habit":
      hdb.incomplete_habits()
      name = questionary.text("Habit name: ").ask()
      hdb.complete_habit(name)
    
    case "Delete all habits":
      hdb.delete_all()

    case "View habit list":
      category = questionary.select(
        "Choose a category: ",
        choices=[
          'Daily',
          'Weekly',
          'All'
        ]
      ).ask()

      match category:

        case 'Daily':
          hdb.print_habits('Daily')

        case 'Weekly':
          hdb.print_habits('Weekly')

        case 'All':
          hdb.print_habits('All')

    case "View longest streak of a habit":
      hdb.print_habits('All')
      name = questionary.text("Habit name: ").ask()
      hdb.longest_streak(name)

    case "View longest streak of all habits":
      hdb.all_longest_streaks()

    case "Load examples":
      hdb.examples()

    case "Close app":
      start = False
      hdb.close_connection()
      print('Have a good day (＾▽＾)')