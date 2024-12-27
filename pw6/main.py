import pickle
import os
import curses
from domain.student import Student
from domain.course import Course
import input
from output import display_list, display_message, display_marks, display_sorted_students
def save_students(students,file_path="students.pkl"):
    try:
        with open(file_path,"wb") as f:
            pickle.dump(students,f)
    except Exception as e:
        print(f"An error occurred while saving students: {e}")
def save_courses(courses,file_path="courses.pkl"):
    try:
        with open(file_path,"wb") as f:
            pickle.dump(courses,f)
    except Exception as e:
        print(f"An error occurred while saving courses: {e}")
def save_marks(courses, file_path="marks.pkl"):
    try:
        marks_data = {course.id: course.mark for course in courses}
        with open(file_path, "wb") as f:
            pickle.dump(marks_data, f)
        print(f"Marks saved to {file_path}.")
    except Exception as e:
        print(f"An error occurred while saving marks: {e}")
def load_students(students,file_path='students.pkl'):
    if os.path.exists(file_path):
        try:
            with open(file_path,'rb') as f:
                loaded_students=pickle.load(f)
                students.extend(loaded_students)
        except (pickle.UnpicklingError, EOFError):
            print(f"Error: File '{file_path}' is corrupted or not a valid pickle file.")
        except Exception as e:
            print(f"Unexpected error while loading students: {e}") 
def load_courses(courses,file_path='courses.pkl'):
    if os.path.exists(file_path):
        try:
            with open(file_path,'rb') as f:
                loaded_courses=pickle.load(f)
                courses.extend(loaded_courses)
        except (pickle.UnpicklingError, EOFError):
            print(f"Error: File '{file_path}' is corrupted or not a valid pickle file.")
        except Exception as e:
            print(f"Unexpected error while loading courses: {e}") 
def load_marks(courses, file_path='marks.pkl'):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                marks_data = pickle.load(f)  

            for course_id, marks in marks_data.items():
                course = next((c for c in courses if c.id == course_id), None)
                if course:
                    course.marks.update(marks)
            print(f"Successfully loaded marks from {file_path}.")
        except (pickle.UnpicklingError, EOFError):
            print(f"Error: File '{file_path}' is corrupted or not a valid pickle file.")
        except Exception as e:
            print(f"Unexpected error while loading marks: {e}")
    else:
        print(f"File '{file_path}' does not exist.")
def main(stdscr):
    students = []
    courses = []
    load_students(students)
    load_courses(courses)
    load_marks(courses)
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
            elif choice == "8":    
                save_students(students)
                save_courses(courses)
                save_marks(courses)
                break
            else:
                display_message(stdscr, "Invalid choice! Please try again.")
        except Exception as e:
            display_message(stdscr, f"An error occurred: {str(e)}")
if __name__ == "__main__":
    curses.wrapper(main)
