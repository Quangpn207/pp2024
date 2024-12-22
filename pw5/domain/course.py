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