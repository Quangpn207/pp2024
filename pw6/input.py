import curses
import math
from domain.student import Student
from domain.course import Course
def input_popup(stdscr, prompt):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    user_input = stdscr.getstr(1, 0).decode("utf-8").strip()
    curses.noecho()
    return user_input
def input_student(student, stdscr):
    num_students = int(input_popup(stdscr, "Enter number of students: "))
    for i in range(num_students):
        id = input_popup(stdscr, f"Enter Student {i+1} ID: ")
        name = input_popup(stdscr, f"Enter Student {i+1} Name: ")
        dob = input_popup(stdscr, f"Enter Student {i+1} DoB: ")
        student_obj = Student(id, name, dob)
        student.append(student_obj)
def input_course(course,stdscr):   
    num_courses = int(input_popup(stdscr, "Enter number of courses: "))
    for i in range(num_courses):
        course_id = input_popup(stdscr, f"Enter Course {i+1} ID: ")
        course_name = input_popup(stdscr, f"Enter Course {i+1} Name: ")
        course_credits = int(input_popup(stdscr, f"Enter Credits for Course {i+1}: "))
        course_obj=Course(course_id, course_name, course_credits)
        course.append(course_obj)
def input_mark(student,course, stdscr):
    course_id = input_popup(stdscr, "Enter Course ID to assign marks: ")
    course = next((c for c in course if c.id == course_id), None)
    if not course:
        stdscr.clear()
        stdscr.addstr(0, 0, "Course not found! Press any key to return.")
        stdscr.refresh()
        stdscr.getch()
        return
    for student in student:
        mark = float(input_popup(stdscr, f"Enter mark for {student.name} ({student.id}): "))
        if 0 <= mark <= 20:
            course.assign_mark(student.id, math.floor(mark))
        else:
            stdscr.clear()
            stdscr.addstr(0, 0, "Invalid mark! Press any key to return.")
            stdscr.refresh()
            stdscr.getch()