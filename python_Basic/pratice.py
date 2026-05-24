'''class Dog:
    species = "Canine" #class variable shared by all instances of the class
    def __init__(self, name, age):
        self.name = name #instance variable unique to each instance of the class
        self.age = age

dog1 = Dog("Buddy", 3)
print(dog1.name)
print(dog1.age)


class Students:
    def __init__(self, name, marks,age):
        self.name = name
        self.marks = marks
        self.age = age
        if self.marks >= 40:
            print("Pass")
        else:
            print("Fail")
student1 = Students("Alice", 85, 20)
print(student1.name, student1.marks, student1.age)
student2 = Students("Bob", 35, 19)
print(student2.name, student2.marks, student2.age)


class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.balance = balance
        def deposit(self, amount):
            self.balance += amount
        def withdraw(self, amount):
            if amount <= self.balance:
                self.balance -= amount
            else:
                print("Insufficient funds")
account = BankAccount("John Doe", 1000)
account.deposit(500)
print(account.balance) # Output: 1500
account.withdraw(200)
print(account.balance) # Output: 1300
account.withdraw(1500) # Output: Insufficient funds


class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    def increase_salary(self, percentage):
            self.salary += self.salary * (percentage / 100)
employee1 = Employee("Alice", 50000)
print(employee1.salary)
employee1.increase_salary(80)  
print(employee1.salary) 


class Rectangle:
     def __init__(self, length, width):
          self.length = length
          self.width = width
     def area(self):
           return self.length * self.width
     def perimeter(self):
              return 2 * (self.length + self.width)
rect = Rectangle(5, 3)
print("Area:", rect.area())
print("Perimeter:", rect.perimeter())
'''



ns=[1,2,3,4,5]
for n in ns:
    if n==3:
        break
else:
    print("Loop completed")

