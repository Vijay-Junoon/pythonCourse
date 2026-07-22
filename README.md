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

### 🛠️ 2. Key Concepts & Functions Covered

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

---

## 📅 Day 3: Loops, Control Statements & Practical Examples

On Day 3, we explored loops in Python, learning why loops are necessary, how to use `for` and `while` loops, loop control flow statements (`break` and `continue`), and solved basic practical examples.

### 🔁 1. Why Loops?

Loops allow us to execute a block of code repeatedly without writing repetitive lines of code.

#### ❌ Without Loops (Repetitive Code)
```python
num = 0
print(num)
num += 1
print(num)
num += 1
print(num)
```

#### ✅ With Loops (Clean & Efficient Code)
```python
for num in range(0, 6):
    print(num, end=", ")
```

---

### 🔄 2. Types of Loops

#### 🔂 For Loop
A `for` loop is used to iterate over a sequence (such as a `range()` object, string, or list).

```python
# Iterating over numbers from 0 to 5
for num in range(0, 6):
    print(num, end=", ")
```

#### 🔁 While Loop
A `while` loop executes a block of statements repeatedly as long as the specified condition remains `True`.

```python
# Printing numbers from 0 to 5 using a while loop
num = 0
while num <= 5:
    print(num)
    num += 1
```

##### 🎓 Practical Example: Condition-driven `while` loop
```python
# Student holiday problem
adminMsg = True
while adminMsg != False:
    print("Student goes to college")
    adminMsg = bool(input("College there or not? "))
print("It is a holiday today!")
```

---

### 🛑 3. Loop Control Statements

#### ⏹️ `break` Statement
The `break` statement terminates the loop execution immediately when encountered and shifts execution control to the code after the loop.

```python
# Terminate loop as soon as the target letter is found
word = "apple"
letter = "p"
found = False

for i in range(0, len(word)):
    print(f"Checking! {word[i]}")
    if word[i] == letter:
        found = True
        print(f"Found at index: {i}")
        break  # Exit loop immediately
```

#### ⏭️ `continue` Statement
The `continue` statement skips the rest of the current loop iteration and moves directly to the next iteration.

```python
# Skip even numbers and print only odd numbers
end = 10
for i in range(0, end + 1):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)
```

---

### 💡 4. Basic Examples & Problem Solving

#### 1️⃣ Sum of First `n` Numbers
Calculating the sum of numbers from `1` to `n` using a `for` loop.

```python
n = int(input("Enter value of n: "))
result = 0
for i in range(1, n + 1):
    result += i
print("Sum:", result)
```

#### 2️⃣ Search Character in String (Linear Search)
Using index-based iteration with a `for` loop and `break` to locate a letter in a word.

```python
word = "apple"
letter = input("Enter a letter to be searched! ")
found = False

for i in range(0, len(word)):
    print(f"Checking! {word[i]}")
    if word[i] == letter:
        found = True
        print(f"Found at index: {i}")
        break

if not found:
    print(-1)
```

#### 3️⃣ Iterating Through Characters of a String
Accessing string characters sequentially using index range.

```python
word = input("Enter word: ")
for i in range(0, len(word)):
    print(word[i])
```


---

## 📅 Day 4: Python Lists - Operations & Basic Problems

On Day 4, we explored Python lists in detail, learning how to define them, modify them using built-in methods, perform mathematical and ordering operations, and solve basic list manipulation problems.

### 📋 1. List Definition
A list is a built-in, ordered, and mutable sequence in Python. It can store elements of various data types, including other lists.

```python
# Creating an empty list using list() constructor
nums = list()
print(nums)  # Output: []

# Creating a list using square brackets
nums = [1, 2, 3]
print(nums)  # Output: [1, 2, 3]
```

---

### 🛠️ 2. Key List Operations & Methods

#### ➕ Appending Elements (`append()`)
Adds an element to the end of the list.
```python
nums = [1, 2, 3]
nums.append(4)
print(nums)  # Output: [1, 2, 3, 4]

# Appending a list inside a list (nested list)
nums.append([5, 6])
print(nums)  # Output: [1, 2, 3, 4, [5, 6]]
```

#### 🗑️ Deleting Elements (`pop()` & `remove()`)
- **`pop()`**: Removes and returns the last element of the list (or an element at a specified index).
- **`remove()`**: Removes the first occurrence of a specific value.

```python
# Using pop() to remove the last element
nums = [1, 2, 3, [4, 5, 6]]
nums.pop()
print(nums)  # Output: [1, 2, 3]

# Using remove() to remove a specific item
nums = [1, 2, 3, [4, 5, 6]]
nums.remove([4, 5, 6])
print(nums)  # Output: [1, 2, 3]
```

#### 📥 Inserting Elements (`insert()`)
Inserts an element at a specified index.
```python
nums = [1, 2, 3]
# Insert value 4 at index 1
nums.insert(1, 4)
print(nums)  # Output: [1, 4, 2, 3]
```

#### 📊 Utilities (`len()` & `sum()`)
- **`len()`**: Returns the number of elements in a list.
- **`sum()`**: Calculates the total sum of elements in a numerical list.

```python
nums = [1, 2, 3]
print(len(nums))  # Output: 3
print(sum(nums))  # Output: 6
```

#### 🔢 Sorting (`sort()`)
Sorts the items of the list in-place (ascending by default, or descending if `reverse=True` is provided).
```python
nums = [1, 6, 2, 5, 3, 4]

# Ascending order
nums.sort()
print(nums)  # Output: [1, 2, 3, 4, 5, 6]

# Descending order
nums.sort(reverse=True)
print(nums)  # Output: [6, 5, 4, 3, 2, 1]
```

#### ↩️ Reversing a List using Slicing (`[::-1]`)
Reverses the elements of a list using Python's slicing syntax.
```python
nums = [1, 5, 2, 4, 3]
reversed_nums = nums[::-1]
print(reversed_nums)  # Output: [3, 4, 2, 5, 1]
```

---

### 💡 3. Basic Problems Covered

#### 1️⃣ Build a List from User Input
Taking the number of elements as input and dynamically building a list with user inputs.
```python
n = int(input("Enter n: "))
parent = []

for chance in range(0, n):
    element = int(input("Enter element: "))
    parent.append(element)

print("Constructed list:", parent)
```

#### 2️⃣ Separate Even and Odd Numbers
Iterating through a list of integers and partitioning them into two lists of even and odd numbers.
```python
parent = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even, odd = [], []

for num in parent:
    if num % 2 == 0:
        even.append(num)
    else:
        odd.append(num)

print("Even array: ", *even)  # Output: Even array:  2 4 6 8 10
print(f"Odd: {odd}")          # Output: Odd: [1, 3, 5, 7, 9]
```
=======
>>>>>>> 1925b36d8c8ae39dcd8f32f94ff05ad36a823101
