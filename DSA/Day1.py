'''num = int(input("Enter a number:"))
if num> 0:
    print("positive")
elif num < 0:
    print("negative")
else:
    print("Zero")


a = int(input("Enter a number:"))
b = int(input("Enter another number:"))
c = int(input("Enter another number:"))
if a>b and a>c:
    print("a is greatest")
elif b>a and b>c:
    print("b is greatest")
else:
    print("c is greatest")


ly = int(input("Enter a year:"))
if ly%4==0 and ly%100!=0 or ly%400==0:
    print("leap year")
else:
    print("not a leap year")


a = int(input("Enter a number:"))
sum = 0
for i in range(1,a+1):
    sum = i + sum
print(sum)

fact = int(input("Enter a number:"))
f = 1
for i in range(2,fact+1):
    f = i*f
print(f)


rev = input("Enter a number:")
rev1 = rev[::-1]
print(rev1)


p = int(input("Enter a number:"))
for i in range(1,p):
    if p%11==0:
        print("Palindrome")
        break
    else:
        print("Not a palindrome")
        break


n = input("Enter a number:")
sum = 0
for i in n:
    a = slice(n)
    sum = int(i) + sum
print(sum)'''


n = input("Enter a number:")
sum = 0
for i in n:
    a = slice(n)
    sum = int(i) + sum
print(sum)

