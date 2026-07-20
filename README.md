# Python Course

A repository documenting my learning journey in Python.

---

## 📅 Day 1: Introduction to Python Basics

On Day 1, we covered foundational concepts in Python including variables, standard data types, lists, and basic built-in functions.

### 1. Variables & Data Types
In Python, variables are used to store data, and they do not require explicit declaration. Python automatically determines the data type based on the value assigned.

#### 🔢 Integer
Numbers without decimal points (positive, negative, or zero).
```python
# Examples
a = 10
b = 20
```

#### 📏 Float
Numbers with decimal points.
```python
# Examples
f1 = 1.35
pi = 3.14
```

#### 🔤 String
A collection of characters enclosed within a pair of single (`'`) or double (`"`) quotes.
```python
# Examples
word = "Hello"
sentence = "Hello World"
```

#### ⚖️ Boolean
A logical value representing either `True` or `False`.
```python
# Examples
adult = True
male = False
```

#### 📋 List
A collection of ordered and mutable elements enclosed within a pair of square brackets `[]`.
```python
# Examples
list1 = [1, 2, 3, 4, 5]
```

---

### 🛠️ Key Concepts & Functions Covered

#### 📐 Length of a List (`len()`)
The `len()` function returns the number of items (length) in an object, such as a list or a string.
```python
# Example
my_list = [1, 2, 3, 4, 5]
list_length = len(my_list) # Returns 5
print(list_length)
```

#### ➕ Sum of a List (`sum()`)
The `sum()` function returns the sum of all elements in an iterable (like a list) containing numbers.
```python
# Example
my_list = [1, 2, 3, 4, 5]
list_sum = sum(my_list) # Returns 15 (1 + 2 + 3 + 4 + 5)
print(list_sum)

```

---

## 📅 Day 2: Operators, Control Flow & Problem Solving

On Day 2, we covered various Python operators (arithmetic, relational, logical, membership, and assignment), `if-elif-else` conditional statements, and solved practical beginner problems.

### 🧮 1. Python Operators

Operators are special symbols used to perform operations on variables and values.

#### ➕ Arithmetic Operators
Used to perform mathematical operations.
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division (returns float)
- `//` Floor Division (truncates decimal)
- `%` Modulus (returns remainder)
- `**` Exponentiation (power)

```python
a = 20
b = 10

print(a + b)   # Output: 30
print(a - b)   # Output: 10
print(a * b)   # Output: 200
print(a / b)   # Output: 2.0
print(a // b)  # Output: 2
print(a ** b)  # Output: 102400000000000000000
```

#### 🔍 Relational (Comparison) Operators
Used to compare two values. Returns either `True` or `False`.
- `>` Greater than
- `<` Less than
- `==` Equal to
- `>=` Greater than or equal to
- `<=` Less than or equal to
- `!=` Not equal to

```python
a = 0
b = 1

print(a > b)   # Output: False
print(a < b)   # Output: True
print(a == b)  # Output: False
print(a >= b)  # Output: False
print(a <= b)  # Output: True
print(a != b)  # Output: True
```

#### 🧠 Logical Operators
Used to combine conditional statements.
- `and` Returns `True` if both statements are true
- `or` Returns `True` if one of the statements is true
- `not` Reverses the result, returns `False` if the result is true

```python
a = True
b = False

print(not a)       # Output: False
print(a and b)     # Output: False
print(a or b)      # Output: True
```

#### 🔤 Membership Operators
Used to test if a sequence (like a string or list) is present in an object.
- `in` Returns `True` if value is present in the sequence
- `not in` Returns `True` if value is not present in the sequence

```python
word = "Hello"

print("e" in word)      # Output: True
print("e" not in word)  # Output: False
```

#### 📝 Assignment Operators
Used to assign values to variables.
- `=` Simple assignment
- `+=` Add and assign (`a += b` is equivalent to `a = a + b`)
- `-=` Subtract and assign
- `*=` Multiply and assign
- `/=` Divide and assign

```python
a = 10
a = a + 15  # a becomes 25
print(a)

a = 10
a *= 5      # a becomes 50
print(a)
```

---

### 🔀 2. Conditional Statements (`if`, `elif`, `else`)

Conditional statements allow decision-making in code based on specified boolean conditions.

```python
if condition1:
    # block executed if condition1 is True
elif condition2:
    # block executed if condition2 is True
else:
    # block executed if all conditions above are False
```

---

### 💡 3. Problem Solving Questions Covered

#### 1️⃣ Check Adult Status
Determining if a person is an adult based on age input.
```python
age = int(input("Please enter your age: "))
if age >= 18:
    print("Adult")
else:
    print("Not an Adult")
```

#### 2️⃣ Check Even or Odd Number
Using the modulus operator `%` to check if a number is divisible by 2.
```python
num = int(input("Enter a number: "))
if num % 2 == 0:
    print("Even")
else:
    print("Odd")
```

#### 3️⃣ Check Exam Result (Pass / Fail)
Comparing obtained marks against a passing threshold.
```python
passing_marks = 35
marks_obtained = int(input("Enter your marks: "))

if marks_obtained <= passing_marks:
    print("Sorry. You have Failed!")
else:
    print("Yayy! You have passed!")
```

#### 4️⃣ Check Range of a Number
Categorizing numbers into range brackets using logical `and` combined with `elif` conditions.
```python
num = int(input("Enter a number between 0 and 100: "))

if num >= 0 and num <= 20:
    print("Number less than 20.")
elif num >= 21 and num <= 60:
    print("Number less than 60.")
else:
    print("Number less than 100.")
```
```
