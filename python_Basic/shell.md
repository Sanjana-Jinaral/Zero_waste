# PS E:\Studyjs\python_Basic> python
# Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information. 
# Ctrl click to launch VS Code Native REPL
# >>> print
# <built-in function print>
# >>> print("hello") 
# hello
# >>> "hello"*3
# 'hellohellohello'
# >>> score=111111
# >>> score
# 111111
# >>> import os
# >>> os.getcwd()
# 'E:\\Studyjs\\python_Basic'
# >>> for c in "chai":
# ... print(c) 
#   File "<stdin>", line 2
#     print(c)
#     ^
# IndentationError: expected an indented block after 'for' statement on line 1
# >>> for c in "chai":
# ...      print(c)
# ...
# c
# h
# a
# i
# >>> import sys
# >>> sys.platform
# 'win32'
# >>> import hello
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ModuleNotFoundError: No module named 'hello'
# >>> import basic1   
# hello world!
# apple
# >>> basic1.hello("world") 
# world
# >>> basic1.hello1        
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: module 'basic1' has no attribute 'hello1'. Did you mean: 'hello'?
# >>> import basic1 
# >>> basic1.hello1 
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: module 'basic1' has no attribute 'hello1'. Did you mean: 'hello'?
# >>> from importlib import reload
# >>> reload(basic1) 
# hello world!
# apple
# <module 'basic1' from 'E:\\Studyjs\\python_Basic\\basic1.py'>
# >>> basic1.hello1
# 'mango'
# >>>usrnm = 'sam'
#  >>> dir(usrnm)
# ['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
# >>>(it is used as help)





<!-- >>> import sys
>>> sys.getrefcount(24601)
3
>>> sys.getrefcount("sam") 
3
>>> sys.getrefcount("x")   
1000000029
>>>  -->

<!-- >>> h1=[1,2,3]
>>> h2=h1[:]
>>> h1
[1, 2, 3]
>>> h2
[1, 2, 3]
>>> h1[0]=55
>>> h1       
[55, 2, 3]
>>> h2       
[1, 2, 3]
>>>import copy
>>> h2=copy.copy(h1) only copy main list
>>> h2=copy.deepcopy(h1) can copy all insidelist-->

<!-- n=[1,2,3]
>>> m=n
>>> m
[1, 2, 3]
>>> n
[1, 2, 3]
>>> m==n
True
>>> m is n
True
>>> m=[1,2,3]   
>>> m==n
True
>>> m is n
False
>>> -->