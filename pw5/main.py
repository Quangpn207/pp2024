import zipfile
import os
import curses
from domain.student import Student
from domain.course import Course
import input
from output import display_list, display_message, display_marks, display_sorted_students

def compress_files(file_paths, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_paths:
            zipf.write(file, arcname=file.split("/")[-1])  # Add each file to the zip
    print(f"Compressed {len(file_paths)} files into {zip_path}")
def decompress_files(zip_file_path, extract_to):
    try:
        os.makedirs(extract_to,exist_ok=True)
        with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
            zip_ref.extractall(extract_to)
            return zip_ref.namelist()
    except FileNotFoundError:
        return []
    except zipfile.BadZipFile:
        return []
def load_students(file_path):
    students = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(", ")
                    student_id = parts[0].split(": ")[1]
                    name = parts[1].split(": ")[1]
                    dob = parts[2].split(": ")[1]
                    students.append(Student(student_id, name, dob))
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return students
def load_courses(file_path):
    courses = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(", ")
                    course_id = parts[0].split(": ")[1]
                    name = parts[1].split(": ")[1]
                    credits = int(parts[2].split(": ")[1])
                    courses.append(Course(course_id, name, credits))
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return courses
def load_marks(file_path, courses):
    try:
        with open(file_path, "r") as f:
            current_course = None
            for line in f:
                line = line.strip()
                if line.startswith("Mark for course"):
                    course_name = line.split("Mark for course ")[1].rstrip(":")
                    current_course = next((c for c in courses if c.name == course_name), None)
                elif current_course:
                    parts = line.split(": ")
                    if len(parts) == 2:
                        student_info, mark = parts
                        student_id = student_info.split("(")[1].rstrip(")")
                        current_course.assign_mark(student_id, float(mark))
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
import os

def delete_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                os.remove(file_path) 
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

def main(stdscr):
    students = []
    courses = []
    zip_file_path = "students.dat"
    extract_to = "."
    if os.path.exists(zip_file_path):
        decompress_files(zip_file_path,extract_to)
    students = load_students("students.txt")
    courses = load_courses("courses.txt")
    load_marks("marks.txt", courses)
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
                    display_sorted_students(stdscr, "Sorted Students by GPA:", student_gpa_list)
            elif choice == "8":  # Exit
                files = [
                    "students.txt",
                    "courses.txt",
                    "marks.txt"
                    ]
                existing_files = [file for file in files if os.path.exists(file)]
                if existing_files:
                    compress_files(existing_files, "students.dat")
                    delete_files(existing_files)
                    print(f"Compressed and deleted files: {existing_files}")
                else:
                    print("No files to compress or delete.")
                break
            else:
                display_message(stdscr, "Invalid choice! Please try again.")
        except Exception as e:
            display_message(stdscr, f"An error occurred: {str(e)}")
if __name__ == "__main__":
    curses.wrapper(main)
