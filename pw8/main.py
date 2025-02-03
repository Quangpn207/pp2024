import pickle
import os
import gzip
import threading
import curses
from queue import Queue
from domain.student import Student
from domain.course import Course
import input
from output import display_list, display_message, display_marks, display_sorted_students

data_queue = Queue()

def async_save_worker():
    """ Background worker to process data saving requests."""
    while True:
        file_path, data = data_queue.get()
        if file_path is None:  # Stop signal
            break
        try:
            with gzip.open(file_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Error saving {file_path}: {e}")
        data_queue.task_done()

def start_async_saving():
    """ Start the background saving thread. """
    thread = threading.Thread(target=async_save_worker, daemon=True)
    thread.start()
    return thread

def save_data_async(data, file_path):
    """ Queue data for asynchronous saving. """
    data_queue.put((file_path, data))

def save_students(students, file_path="students.pkl.gz"):
    save_data_async(students, file_path)

def save_courses(courses, file_path="courses.pkl.gz"):
    save_data_async(courses, file_path)

def save_marks(courses, file_path="marks.pkl.gz"):
    marks_data = {course.id: course.mark for course in courses}
    save_data_async(marks_data, file_path)

def load_data(file_path):
    """ Load data from a compressed pickle file. """
    if os.path.exists(file_path):
        try:
            with gzip.open(file_path, 'rb') as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, EOFError, OSError):
            print(f"Error: File '{file_path}' is corrupted or not a valid pickle file.")
        except Exception as e:
            print(f"Unexpected error while loading {file_path}: {e}")
    return []

def load_students(students, file_path='students.pkl.gz'):
    students.extend(load_data(file_path) or [])

def load_courses(courses, file_path='courses.pkl.gz'):
    courses.extend(load_data(file_path) or [])

def load_marks(courses, file_path='marks.pkl.gz'):
    marks_data = load_data(file_path)
    if isinstance(marks_data, dict):
        for course_id, marks in marks_data.items():
            course = next((c for c in courses if c.id == course_id), None)
            if course:
                course.mark.update(marks)

def initialize_data():
    """ Load all data at the beginning of the program. """
    students = []
    courses = []
    load_students(students)
    load_courses(courses)
    load_marks(courses)
    return students, courses

save_thread = start_async_saving()

def stop_saving():
    data_queue.put((None, None))  # Stop signal
    save_thread.join()

def main(stdscr):
    students, courses = initialize_data()
    
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
            if choice == "1":
                input.input_student(students, stdscr)
            elif choice == "2":
                input.input_course(courses, stdscr)
            elif choice == "3":
                input.input_mark(students, courses, stdscr)
            elif choice == "4":
                display_list(stdscr, "Students:", [str(student) for student in students])
            elif choice == "5":
                display_list(stdscr, "Courses:", [str(course) for course in courses])
            elif choice == "6":
                course_id = input.input_popup(stdscr, "Enter Course ID to view marks: ")
                course = next((c for c in courses if c.id == course_id), None)
                if course:
                    marks = [f"{student.name} ({student.id}): {course.mark.get(student.id, 'N/A')}" for student in students]
                    display_marks(stdscr, f"Marks for {course.name}:", marks)
                else:
                    display_message(stdscr, "Course not found!")
            elif choice == "7":
                student_gpa_list = []
                for student in students:
                    total_marks = [course.mark.get(student.id, 0) * course.credits for course in courses]
                    total_credits = [course.credits for course in courses if student.id in course.mark]
                    gpa = sum(total_marks) / sum(total_credits) if total_credits else 0
                    student_gpa_list.append(f"{student.name} (ID: {student.id}): GPA = {round(gpa, 2)}")
                student_gpa_list.sort(key=lambda x: float(x.split("GPA = ")[1]), reverse=True)
                display_sorted_students(stdscr, "Sorted Students by GPA:", student_gpa_list)
            elif choice == "8":    
                save_students(students)
                save_courses(courses)
                save_marks(courses)
                stop_saving()
                break
            else:
                display_message(stdscr, "Invalid choice! Please try again.")
        except Exception as e:
            display_message(stdscr, f"An error occurred: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main)
