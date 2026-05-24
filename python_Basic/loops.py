# Counting Positive Numbers
# numbers = [1, -2, 3, -4, 5, -6 , -7, -8, 9, 10]
# positive_number_count = 0
# for num in numbers:
#     if num > 0:
#         positive_number_count += 1
# print("Final count of positive numbers:", positive_number_count)

#  Sum of Even Numbers
# n = 10
# sum_even = 0
# for i in range(1,n+1):
#     if i%2 == 0:
#         sum_even += i
# print("Sum of even numbers is:", sum_even)

# Multiplication Table except 5
# num = 3
# for i in range(1,11):
#     if i == 5:
#         continue
#     print(num, 'x', i , '=', num*i)

# reverse the String
# string = "Python"
# reversed_str =""
# for char in string:
#     reversed_str = char + reversed_str
# print(reversed_str)

#first not repiting character
# input_str = "teeterababc"
# for char in input_str:
#     print(char)
#     if input_str.count(char) == 1:
#         print("Character:", char)
#         break


# Factorial of a number
# number = 5
# factorial = 1
# while number > 0:
#     factorial *= number
#     number -= 1
# print("Factorial is:", factorial)
# 5*4=20
# 20*3=60
# 60*2=120
# 120*1=120

# Validate Input
# Problem: Keep asking the user for input until they enter a number between 1 and 10.
# while True:
#     number = int(input("Enter a number between 1 and 10: "))
#     if 1 <= number <= 10:
#         print("Thank you for entering a valid number:", number)
#         break
#     else:
#         print("Invalid input. Please try again.")

# prime number checker
# number = 29
# is_prime = True
# if number > 1:
#     for i in range(2, number):
#         if (number % i) == 0:
#             is_prime = False
#             break
# print(number, "is a prime number:", is_prime)

#List Uniqueness checker
# Problem: Check if all elements in a list are unique.If a duplicate is found, exit the loop and print the duplicate.
# items = ["apple", "bannana", "orange", "apple", "mango"]
# items = ["apple", "bannana", "orange", "apple", "mango"]
# unique_items = set()
# for item in items:
#     if item in unique_items:
#         print("Duplicate found:", item)
#         break
#     unique_items.add(item)

# Expontential backoff
# Problem: Implement an exponential backoff strategy that doubles the wait time between retries, starting from 1 second, and stops after 5 retries.
import time
wait_time = 1
max_retries = 5
attempts = 0

while attempts < max_retries:
    print("Attempt", attempts + 1, "- waittime", wait_time, "seconds")
    time.sleep(wait_time)  # Simulate waiting
    wait_time *= 2  # Double the wait time
    attempts += 1