import curses
def display_list(stdscr, title, items):
    stdscr.clear()
    stdscr.addstr(0, 0, title)
    for idx, item in enumerate(items, start=1):
        stdscr.addstr(idx, 0, str(item))
    stdscr.addstr(len(items) + 2, 0, "Press any key to return.")
    stdscr.refresh()
    stdscr.getch()
def display_marks(stdscr, title, marks):
    stdscr.clear()
    stdscr.addstr(0, 0, title)
    for idx, mark in enumerate(marks, start=1):
        stdscr.addstr(idx, 0, mark)
    stdscr.addstr(len(marks) + 2, 0, "Press any key to return.")
    stdscr.refresh()
    stdscr.getch()
def display_message(stdscr, message):
    stdscr.clear()
    stdscr.addstr(0, 0, message)
    stdscr.addstr(2, 0, "Press any key to return.")
    stdscr.refresh()
    stdscr.getch()
def display_sorted_students(stdscr, title, students):
    stdscr.clear()
    stdscr.addstr(0, 0, title)
    for idx, student in enumerate(students, start=1):
        stdscr.addstr(idx, 0, student)
    stdscr.addstr(len(students) + 2, 0, "Press any key to return.")
    stdscr.refresh()
    stdscr.getch()
