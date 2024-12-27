import curses
import numpy as np
from domain.student import Student
from domain.course import Course
import input
from output import display_list, display_message, display_marks, display_sorted_students


def main(stdscr):
    students = []
    courses = []

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Menu:")
        stdscr.addstr(1, 0, "1. Input Students")
        stdscr.addstr(2, 0, "2. Input Courses")
        stdscr.addstr(3, 0, "3. Input Marks")
        stdscr.addstr(4, 0, "4. List Students")
        stdscr.addstr(5, 0, "5. List Courses")
        stdscr.addstr(6, 0, "6. List Marks for a Course")
        stdscr.addstr(7, 0, "7. Sort Students by GPA")
        stdscr.addstr(8, 0, "8. Exit")
        stdscr.addstr(9, 0, "Enter your choice: ")
        stdscr.refresh()

        curses.echo()
        choice = stdscr.getstr(10, 0).decode("utf-8").strip()
        curses.noecho()

        try:
            if choice == "1":  # Input Students
                input.input_student(students, stdscr)
            elif choice == "2":  # Input Courses
                input.input_course(courses, stdscr)
            elif choice == "3":  # Input Marks
                input.input_mark(students, courses, stdscr)
            elif choice == "4":  # List Students
                if not students:
                    display_message(stdscr, "No students found!")
                else:
                    display_list(stdscr, "Students:", [str(student) for student in students])
            elif choice == "5":  # List Courses
                if not courses:
                    display_message(stdscr, "No courses found!")
                else:
                    display_list(stdscr, "Courses:", [str(course) for course in courses])
            elif choice == "6":  # List Marks for a Course
                if not courses:
                    display_message(stdscr, "No courses available!")
                elif not students:
                    display_message(stdscr, "No students available!")
                else:
                    course_id = input.input_popup(stdscr, "Enter Course ID to view marks: ")
                    course = next((c for c in courses if c.id == course_id), None)
                    if course:
                        mark = [
                            f"{student.name} ({student.id}): {course.mark.get(student.id, 'N/A')}"
                            for student in students
                        ]
                        display_marks(stdscr, f"Marks for {course.name}:", mark)
                    else:
                        display_message(stdscr, "Course not found!")
            elif choice == "7":  # Sort Students by GPA
                if not students or not courses:
                    display_message(stdscr, "Not enough data to calculate GPA!")
                else:
                    student_gpa_list = []
                    for student in students:
                        total_marks = []
                        total_credits = []
                        for course in courses:
                            if student.id in course.mark:
                                total_marks.append(course.mark[student.id] * course.credits)
                                total_credits.append(course.credits)
                        if total_credits:
                            gpa = sum(total_marks) / sum(total_credits)
                            student_gpa_list.append(f"{student.name} (ID: {student.id}): GPA = {round(gpa, 2)}")
                    student_gpa_list.sort(key=lambda x: float(x.split("GPA = ")[1]), reverse=True)
                    display_sorted_students(stdscr, "Sorted Students by GPA:", student_gpa_list)
            elif choice == "8":  # Exit
                break
            else:
                display_message(stdscr, "Invalid choice! Please try again.")
        except Exception as e:
            display_message(stdscr, f"An error occurred: {str(e)}")
if __name__ == "__main__":
    curses.wrapper(main)
