class Student:
    def __init__(self,id,name,DoB):
        self.id=id
        self.name=name
        self.DoB=DoB
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, DoB: {self.DoB}"