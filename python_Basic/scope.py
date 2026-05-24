username = "hello world!" #global variable(Accessible everywhere unless shadowed)

def test():
    pass

def func():
    username = "hello" #local variable
    print(username) #hello (function memory)

print(username)#hello world(global memory-- Namespace)
func()
print(username)#hello

# Python uses LEGB Rule: parsing(Parsing means analyzing a piece of code or text to understand its structure and meaning.), lexical scoping(Breaks code into tokens (keywords, variables, operators))
# L → Local
# E → Enclosing
# G → Global
# B → Built-in

# “Why doesn't function change global variable?”
# Answer:"Because Python creates a new local namespace for functions. The variable inside the function shadows the global variable unless explicitly declared using global."


x = 99
# def func2(y):
#     z = x + y
#     return z

# result = func2(1)
# print(result) 


# def func3():
#     global x #declare x as global variable (don't manuplate (overwrite the value))
#     x = 12

# func3() #x = 12 because of global keyword
# print(x) 


x=66
def f1():
    x = 88
    def f2():
        print(x) #88 (enclosing scope of f2 is f1, so it can access x)
    return f2 #returning the function object (closure) return refers the f2 definition
myresult = f1() #calling

#closure: A closure is a function object that has access to variables in its enclosing scope, even after the outer function has finished executing. In this case, f2 is a closure that retains access to the variable x defined in f1's scope.
#fractory function: A factory function is a function that returns another function. In this case, f1 is a factory function that returns the inner function f2.

myresult() #88 (calling the returned function object which has access to x in f1's scope)
print(x) #66 (global variable)
f1()() #88 (calling the returned function object which has access to x in f1's scope)


def hello(num):
    def actual(x):
        return x**num #actual is a closure that retains access to the variable num defined in hello's scope.
    return actual #hello is a factory function that returns the inner function actual.

f = hello(2) #f is a closure that retains access to the variable num defined in hello's scope.
g = hello(3) #g is a closure that retains access to the variable num defined in hello's scope.
print(f(4)) #16 (4**2)
print(g(4)) #64 (4**3)
print(f) #<function hello.<locals>.actual at 0x7f8c8c8c8c8> (function object)
print(g) #<function hello.<locals>.actual at 0x7f8c8c8c8c8> (function object)


# https://www.geeksforgeeks.org/python/python-closures/