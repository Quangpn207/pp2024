import math
import numpy as np
class Student:
    def __init__(self,id,name,DoB):
        self.id=id
        self.name=name
        self.DoB=DoB
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, DoB: {self.DoB}"
    def printStudent(self):
        print(f"ID: {self.id}, Name: {self.name}, DoB: {self.DoB}")

class Course:
    def __init__(self,id,name,credits):
        self.id=id
        self.name=name
        self.credits=credits
        self.mark={}
    def assign_mark(self,student_id,mark):
        self.mark[student_id]=mark
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}"
class Classroom:
    def __init__(self):
        self.student=[]
        self.course=[]
    def input_student(self):
        num_students=int(input("Enter number of student: "))
        for i in range(num_students):
            student_id=input(f"Enter student {i+1} ID: ").strip()
            student_name=input(f"Enter student {i+1} name: ").strip()
            student_dob=input(f"Enter student {i+1} DoB: ").strip()
            self.student.append(Student(student_id,student_name,student_dob))
    def input_course(self):
        num_courses=int(input("Enter number of course: "))
        for i in range(num_courses):
            course_id=input(f"Enter course {i+1} ID: ").strip()
            course_name=input(f"Enter course {i+1} name: ").strip()
            course_credits=int(input(f"Enter number of credits of course: "))
            self.course.append(Course(course_id,course_name,course_credits))
    def find_course(self, course_id):
        for c in self.course:
            if c.id == course_id:
                return c
        return None
    def input_mark(self):
        course_id=input("Enter course ID to assign mark: ")
        course = self.find_course(course_id)
        if not course:
            print('Course no found')
            return
        for student in self.student:
            mark=float(input(f"Enter mark for {student.name} ({student.id}): "))
            if not 0<=mark<=20:
                print("Invalid mark,try again")
                continue
            course.assign_mark(student.id,math.floor(mark))
    def list_students(self):
        print("Students:")
        for student in self.student:
            print(student)
    def list_courses(self):
        print("Courses:")
        for course in self.course:
            print(course)
    def show_mark(self):
        course_id=input("Enter course id to show mark: ")
        course = self.find_course(course_id)
        if not course:
            print('Course no found')
            return
        for student_id,mark in course.mark.items():
            student = next((s for s in self.student if s.id == student_id), None)
            if student:
                print(f"{student.name}(ID: {student.id}): {mark}")
    def calculate_gpa(self,student_id):
        total_marks = []
        total_credits = []
        for course in self.course:
            if student_id in course.mark:
                total_marks.append(course.mark[student_id] * course.credits)
                total_credits.append(course.credits)
        if total_credits:
            gpa = np.sum(total_marks) / np.sum(total_credits)
            return math.floor(gpa)
        return 0    
    def sort_students_by_gpa(self):
        student_gpa_list = [(student,self.calculate_gpa(student.id))for student in self.student]
        student_gpa_list.sort(key=lambda x: x[1], reverse=True)
        print("Students sorted by GPA (descending):")
        for student, gpa in student_gpa_list:
            print(f"{student.name} (ID: {student.id}), GPA: {gpa}")
if __name__ == "__main__":
    classroom = Classroom()
    while True:
        print("\n1. Input students")
        print("2. Input courses")
        print("3. Input marks")
        print("4. List students")
        print("5. List courses")
        print("6. Show marks")
        print("7. Sort students by GPA")
        print("8. Exit")
        try:
            choice = input("Enter your choice: ").strip()  
        except EOFError:
            print("No more input. Exiting the program.")
            break   
        if choice == "1":
            classroom.input_student()
        elif choice == "2":
            classroom.input_course()
        elif choice == "3":
            classroom.input_mark()
        elif choice == "4":
            classroom.list_students()
        elif choice == "5":
            classroom.list_courses()
        elif choice == "6":
            classroom.show_mark()
        elif choice == "7":
            classroom.sort_students_by_gpa()
        elif choice == "8":
            print("Exiting")
            break
        else:
            print("Invalid choice! Please try again.")
