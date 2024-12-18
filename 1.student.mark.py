Courses=[]
Students=[]
Marks={}   
def input_number(args):
    return int(input(f"Enter number of {args}: "))
def input_Student_information():
    student_id=input("Enter Student ID: ")
    student_name=input("Enter Student name: ")
    DoB=input("Enter date of birth: ")
    Students.append({'id':student_id,'name':student_name,'DoB':DoB})
def input_course_information():
    course_id=input("Enter course id: ")
    course_name=input("Enter course name: ")
    Courses.append({'id':course_id,'name':course_name})
def listcourses():
    print("\nList course: \n")
    for course in Courses:
        print(f"Course ID: {course['id']}, Name: {course['name']}")
def liststudents():
    print("\nList of students: \n")
    for student in Students:
        print(f"Student ID: {student['id']}, Name: {student['name']}, Date of Birth: {student['DoB']}")
def input_marks():
    listcourses()
    course_id=input("Enter course ID to input marks: ")
    if course_id not in Marks:
        Marks[course_id]={}
    for student in Students:
        student_id=student['id']
        student_name=student['name']
        mark=float(input(f"Enter mark for {student_name} ID {student_id} :"))
        Marks[course_id][student_id] = mark   
def show_marks():
    listcourses()
    course_id=input("Enter course ID to show marks: ")
    if course_id in Marks:
        print(f"\nMark for Course {course_id}")
        for student_id,mark in Marks[course_id].items():
            student_name = next(student['name'] for student in Students if student['id']==student_id)
            print(f"Student ID: {student_id}, Name: {student_name}, Mark: {mark}")
    else:
        print("No marks available")
def main():
    num_students=input_number("students")
    for _ in range(num_students):
        input_Student_information()
    num_courses=input_number("courses")
    for _ in range(num_courses):
        input_course_information()
    while True:
        choice=input("Enter mark? (Y/N): ")
        if choice=='Y':
            input_marks()
        else:
            break
    while True:
        print("\nOptions: \n")
        print("1. List students\n2. List courses\n3. Show marks for a course\n4. Exits")
        option=int(input("Enter your choice: "))
        if option==1:
            liststudents()
        elif option==2:
            listcourses()
        elif option==3:
            show_marks()
        elif option==4:
            print("\nExit program")
            break
        else:
            print("\nInvalid option,try again")
if __name__ == "__main__":
    main()