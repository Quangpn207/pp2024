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
    def __init__(self,id,name):
        self.id=id
        self.name=name
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
            student_id=input(f"Enter student {i+1} ID: ")
            student_name=input(f"Enter student {i+1} name: ")
            student_dob=input(f"Enter student {i+1} DoB: ")
            self.student.append(Student(student_id,student_name,student_dob))
    def input_course(self):
        num_courses=int(input("Enter number of course: "))
        for i in range(num_courses):
            course_id=input(f"Enter course {i+1} ID: ")
            course_name=input(f"Enter course {i+1} name: ")
            self.course.append(Course(course_id,course_name))
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
            course.assign_mark(student.id,mark)
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

if __name__ == "__main__":
    classroom = Classroom()
    
    while True:
        print("\n1. Input students")
        print("2. Input courses")
        print("3. Input marks")
        print("4. List students")
        print("5. List courses")
        print("6. Show marks")
        print("7. Exit")
        try:
            choice = input("Enter your choice: ").strip()  # Handle extra spaces
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
            print("Exiting")
            break
        else:
            print("Invalid choice! Please try again.")
