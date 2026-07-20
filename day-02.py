# Arithmetic operators
a = 20
b = 10
print(a+b)
print(a-b)
print(a*b)
print(a/b)
print(a//b)
print(a**b)

# Relational Operators
a = 0
b = 1
print(a > b)
print(a < b)
print(a == b)
print(a >= b)
print(a <= b)
print(a != b)

# Logical Operators
a = True
b = False
print(not a)


# Check whether a person is adult or not
age = int(input("Please enter your age: "))
if age >= 18:
  print("true")
else:
  print("false")

# Assignment operators
a = 10
a = a + 15
print(a)
a = 10
a *= 5
print(a)

# Membership operators
word = "Hello"
print("e" not in word)


# Some basic problem solving to understand use case of operators
# Check given number is even or odd
num = int(input("Enter a number:"))
if num%2 == 0:
  print("Even")
else:
  print("odd")

# Check whether a student passed an exam or not
passing_marks = 35
marks_obtained = int(input("Enter your marks: "))
if marks_obtained <= passing_marks:
  print("Sorry. You have Failed!")
else:
 
  print("Yayy! You have passed!")

# Check whether a number lies in a given range or not
num = int(input("Enter a number between 0 and 100 "))
if num >= 0 and num <= 20:
  print("Number less than 20.")
elif num >= 21 and num <= 60:
  print("Number less than 60.")
else:
  print("Number less than 100.")