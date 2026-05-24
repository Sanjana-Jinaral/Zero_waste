# Basic Function Syntax
# Promblem: Write a function to calculate and return the square of a number.
def square(num):
    # print(num**2)  # This will print the square of the number but does not return it.
    return num**2


# square(4) # Output: 16
result = square(5) # Output: 25
# print(result) # Output: None (since the function does not return anything)
print(result) # Output: 25 (since the function now returns the square of the number)


# Function with Multiple Parameters
# Problem: Create a function that takes two numbers as parameters and returns their sum.
def add(a,b):
    return a + b

print(add(2,3)) # Output: 5


# Polymorphism Functions
# Problem: Write a function multiplies two numbers, but can also accept and mulitply strings.
def multiply(x, y):
    return x * y
print(multiply(8,5))
print(multiply('a',5))
print(multiply(5,'a'))

# Function Returning Multiple Values
# Problem: Create a function that returns both the area and circumference of circle given its radius.
from ast import Name
import math
def circle_stats(radius):
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    return area, circumference

a,c = circle_stats(3)
print("Area: ", a, "Circumference: ", c)
print("Area:", round(a,2), "Circumference:", round(c,2))


# Default Parameter Value
# Problem: Write a function that greets a user.If no name is provided, it should greet with a default name.
def greett(name = "Admin"):
    return "Hello, " + name + " !"
print(greett())
# print(greett("chintu"))



# Lambda Function
# Problem: Create a lambda function to compute the cube of a number
cube = lambda x: x**3 #used framework
print(cube(3))

# Function with *args     (accept any number of positional arguments.)
# Problem: Write a function that takes variable number of arguments and return their sum.
def sum_all(*args): #* tells Python to collect arguments. args becomes a tuple inside the function.
    print(args)
    for i in args:  
        print(i*2)
    # return sum(chai) 
    return sum(args) 

print(sum_all(1,2,4,4,4,4,4,4,4,4,4,4))
# print(sum_all(1,2))
# print(sum_all(1,2,4,4,4))

#Function with **kwargs
# Problem: Create a function that accepts any number of keyword arguments and prints them in the format key:value.
# def print_kwargs(Name, power):
#     print("Name ",Name, "Power:", power)

# print_kwargs(Name="shakti", power="blackhole")
# print_kwargs(Name="shakti")
# print_kwargs(Name="shakti", power="blackhole", enemy="mahishasura")
# ********************************************************
def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
print_kwargs(Name="shakti", power="blackhole")
print_kwargs(Name="shakti")
print_kwargs(Name="shakti", power="blackhole", enemy="mahishasura")

# Generator Function with yeild
# Problem: Write a generator function that yeilds even numbers up to a specified limit.

def even_genrator(limit):
    # li=[]
    for i in range(2, limit+1, 2):
        yield i
        # li.append()
for num in even_genrator(10):
    print(num)


# Recursive Function
# Problem: Create a recursive function to calculate the factorial of a number
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)