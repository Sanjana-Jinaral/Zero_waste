import time
print("hello people")
username = "admin"
print(username)

# >>> f = open('iteration_tools.py')
# >>> f.readline()
# 'import time\n'
# >>> f.readline()
# 'print("hello people")\n'
# >>> f.readline()
# 'username = "admin"\n'
# >>> f.readline()
# 'print(username)'
# >>> f.readline()
# ''


# >>> f = open('iteration_tools.py') 
# >>> f.__next__()
# 'import time\n'
# >>> f.__next__()
# 'print("hello people")\n'
# >>> f.__next__()
# 'username = "admin"\n'
# >>> f.__next__()
# 'print(username)\n'
# >>> f.__next__()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# StopIteration



# >>> for line in open('iteration_tools.py'):
# ...     print(line, end="")
# ...
# import time
# print("hello people")
# username = "admin"  
# print(username)>>>



# f = open('iteration_tools.py')         
# >>> while True: 
# ...     line = f.readline()
# ...     if not line: break
# ...     print(line, end="")
# ...
#  import time
# print("hello people")
# username = "admin"
# print(username)

myList = [1, 2, 3, 4, 5]
I = iter(myList)
print(next(I))  # Output: 1 start ref
print(next(I))  # Output: 2
print(next(I))  # Output: 3 
print(next(I))  # Output: 4
print(next(I))  # Output: 5
# print(next(I))  # This will raise StopIteration as there are no more items to iterate over.


# in functions
f = open('iteration_tools.py')
iter(f) is f #True
iter(f) is f.__iter__() #True


mynewlist = [1, 2, 3]
iter(mynewlist) is mynewlist #False


D = {'a': 1, 'b': 2}
for key in D.keys():
    print(key) 
# Output: a
#         b   

I = iter(D)
print(I)
# Output: <dict_keyiterator object at 0x7f8b8c2e5d30>
print(next(I))  # Output: 'a'
print(next(I))  # Output: 'b'
# print(next(I))  # This will raise StopIteration as there are no more items to


range(5) # range object is an iterable
range(0,5)
R = range(5)
I = iter(R)
print(next(I))  # Output: 0 
print(next(I))  # Output: 1
print(next(I))  # Output: 2
print(next(I))  # Output: 3
print(next(I))  # Output: 4
print(next(I))  # This will raise StopIteration as there are no more items to iterate over.
