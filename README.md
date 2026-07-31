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

---

## 📅 Day 5: Python Dictionaries - Basics & Anagram Problem

On Day 5, we explored Python dictionaries, learning the basics of key-value pairs, key insertion, updation, deletion, and essential methods like `.keys()` and `.values()`. We also solved the Anagram problem using dictionaries.

### 📖 1. What is a Dictionary?
A dictionary is an ordered (as of Python 3.7) and mutable collection of key-value pairs. In a dictionary, keys must be unique and immutable (such as strings, numbers, or tuples), while values can be of any data type and can repeat.

```python
# Creating a dictionary
student = {
    "s_id": 100,
    "name": "Ajay",
    "marks": [85, 90, 92],
    "contact": {"dad": 1234567890, "mom": 9876543210}
}
```

---

### 🛠️ 2. Key Dictionary Operations

#### 📥 Insertion & Updation
We insert new keys or update existing keys using the square bracket notation `[]`.
- If the key does not exist in the dictionary, a new key-value pair is inserted.
- If the key already exists, its value is updated.

```python
d = {}

# Inserting new keys
d['name'] = "Ajay"
d['age'] = 20
print(d)  # Output: {'name': 'Ajay', 'age': 20}

# Updating an existing key
d['age'] = 21
print(d)  # Output: {'name': 'Ajay', 'age': 21}
```

#### 🗑️ Deletion
We can remove key-value pairs from a dictionary using the `del` keyword or the `.pop()` method.
- **`del d[key]`**: Deletes the key-value pair. Raises a `KeyError` if the key does not exist.
- **`d.pop(key)`**: Deletes the key-value pair and returns its value.

```python
d = {'name': 'Ajay', 'age': 21, 'city': 'Mumbai'}

# Using del keyword
del d['city']
print(d)  # Output: {'name': 'Ajay', 'age': 21}

# Using pop() method
age = d.pop('age')
print(age)  # Output: 21
print(d)    # Output: {'name': 'Ajay'}
```

---

### 🔍 3. Built-in Methods: `.keys()` & `.values()`

- **`.keys()`**: Returns a view object containing all the keys of the dictionary.
- **`.values()`**: Returns a view object containing all the values of the dictionary.

```python
d = {'name': 'Ajay', 'age': 21, 'role': 'Student'}

# Get all keys
print(d.keys())    # Output: dict_keys(['name', 'age', 'role'])

# Get all values
print(d.values())  # Output: dict_values(['Ajay', 21, 'Student'])

# Iterating through keys and values
for key in d.keys():
    print(f"Key: {key}")

for val in d.values():
    print(f"Value: {val}")
```

---

### 💡 4. Anagram Problem Using Dictionaries

An **Anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once (e.g., *listen* and *silent*).

#### 🧮 Solution Strategy
We can determine if two words are anagrams by checking if their character frequency distributions are identical. We construct a frequency dictionary for both words using the `.get()` method to handle missing keys gracefully, then compare the two dictionaries.

```python
# Check if two words are anagrams
w1 = input("Enter word 1: ")
w2 = input("Enter word 2: ")

d1 = {}
d2 = {}

# Populate frequency dictionary for word 1
for ch in w1:
    d1[ch] = d1.get(ch, 0) + 1

# Populate frequency dictionary for word 2
for ch in w2:
    d2[ch] = d2.get(ch, 0) + 1

# Compare the two dictionaries
if d1 == d2:
    print("Anagram")
else:
    print("Not Anagram")
```

---

## 📅 Day 7: Python Functions (Week 2)

On Day 7, we introduced functions in Python. We covered function definitions, function calls, parameters, arguments, return statements, and walked through several illustrative examples.

### 🧩 1. What is a Function?
A function is a block of organized, reusable code that is used to perform a single, related action. Functions provide better modularity for your application and a high degree of code reusing.

---

### ✍️ 2. Function Definition & Function Call

#### 🔹 Function Definition
To define a function, use the `def` keyword followed by the function name and parentheses `()`. Any input parameters or arguments should be placed within these parentheses.
```python
def greet(text_message):
    print(text_message)
```

#### 🔹 Function Call
To execute the function, call it by its name followed by parentheses containing the required arguments.
```python
greet(54)
```

---

### 📥 3. Parameters vs. Arguments
- **Parameters**: The variables listed inside the parentheses in the function definition. They act as placeholders for the data the function needs.
- **Arguments**: The actual values passed to the function when it is called.

---

### 📤 4. Return Statements
The `return` statement is used to exit a function and pass a value back to the caller.
```python
def add(a, b):
    s = a + b
    return s

sum1 = add(1, 2)
sum2 = add(sum1, 3)
print(sum2)  # Output: 6
```

---

### 💡 5. Practical Examples Covered

#### 1️⃣ Count Positive Numbers in a List
A function that counts and returns the number of positive elements in a list.
```python
def countPos(user_list):
    pos = 0
    for i in user_list:
        if i > 0:
            pos += 1
    return pos

l1 = [0, -1, 1, 2, 3]
l2 = [0, -1, -2, 3, 5]

pos_l1 = countPos(l1)
pos_l2 = countPos(l2)

if pos_l1 == pos_l2:
    print("Same Pos Nums")
else:
    print("No")
```

#### 2️⃣ Check Even or Odd (with User Input)
A function that checks if a number is even or odd, takes input from the user, and prints the result.
```python
def even_odd(val):
    if val % 2 == 0:
        return f"Number {val} is even"
    else:
        return f"Number {val} is odd"

val1 = int(input("Enter the number: "))
result = even_odd(val1)
print(result)
```

---

## 📅 Day 8: Scope (Local vs. Global Variables) & Function Annotations

On Day 8, we covered variable scopes (local vs. global), function annotations (type hints), and walked through two basic practical examples: Palindrome Checking and Factorial Computation.

### 🌐 1. Local vs. Global Variables

In Python, the scope of a variable refers to the region of the program where a variable is recognized and can be accessed.

#### 🏠 Local Variables
Variables defined inside a function are local to that function. They are created when the function starts executing and are destroyed when the function returns. They cannot be accessed from outside the function.

```python
def my_function():
    x = 10  # Local variable
    print("Inside function:", x)

my_function()
# print(x)  # This will raise a NameError because x is local to my_function
```

#### 🌍 Global Variables
Variables defined outside of any function are global variables. They can be accessed from anywhere within the program, including inside functions (for reading).

```python
y = 20  # Global variable

def print_y():
    print("Inside function:", y)  # Accessing global variable

print_y()
print("Outside function:", y)
```

#### 🔑 Modifying Global Variables (`global` Keyword)
To modify a global variable inside a function, you must declare it using the `global` keyword.

```python
counter = 0  # Global variable

def increment():
    global counter  # Declare intention to modify the global variable
    counter += 1

increment()
print(counter)  # Output: 1
```

---

### 🏷️ 2. Function Annotations

Function annotations are optional metadata about the types used by user-defined functions. They act as **type hints** to specify what type of arguments a function expects and what type it returns. Python ignores them at runtime, but they are highly useful for documentation and static analysis tools.

#### ✍️ Syntax:
- **Parameter Annotations**: `parameter: type`
- **Return Annotation**: `-> type`

```python
# Annotation indicates name is a string, age is an integer, and the function returns a string
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age}."
```

---

### 💡 3. Basic Examples Covered

#### 1️⃣ Palindrome Checking
A basic example demonstrating string slicing to check if a word is a palindrome, using function annotations.

```python
# Function with type annotations
def palindromeChecker(word: str) -> bool:
    # 'word' is a local variable/parameter
    is_palindrome = (word == word[::-1])  # 'is_palindrome' is a local variable
    return is_palindrome

# 'userInput' is a global variable
userInput = input("Enter a word: ")
if palindromeChecker(userInput):
    print("Yes it's a palindrome")
else:
    print("No it's not a palindrome")
```

#### 2️⃣ Compute Factorial
A function to compute the factorial of a number using a loop, demonstrating local variable accumulator and annotations.

```python
# Function with type annotations.
# Note: In our script, we return a string message if input is invalid,
# so the return type can be either int or str.
def computeFactorial(n: int) -> int | str:
    # 'n' is a local parameter
    if n < 0:
        return "Please enter a value greater than or equal to 0"
    
    fact = 1  # 'fact' is a local variable
    for i in range(1, n + 1):  # 'i' is a local loop variable
        fact *= i

    return fact

# 'n' is a global variable in the main block
n = int(input("Enter a number: "))
print(f"Factorial of {n} is: {computeFactorial(n)}")
```

---

## 📅 Day 9: Nested Functions & ATM Simulation Example

On Day 9, we covered **nested functions** (also known as **inner functions**), their scope, and implemented an ATM simulation program to demonstrate how multiple nested functions can be structured inside a single parent function.

### 🧩 1. What is a Nested Function?

A **nested function** is a function defined inside another function. In Python, functions are first-class citizens, meaning they can be defined anywhere, passed as arguments, and returned from other functions.

#### 🔹 Syntax
```python
def outer_function():
    # Outer function scope
    def inner_function():
        # Inner function scope
        pass
    inner_function()  # Call the inner function inside the outer function
```

#### 🔑 Key Characteristics:
1. **Encapsulation & Information Hiding**: The inner function is not accessible from the global scope. It is hidden and only exists within the scope of the outer function.
2. **Access to Outer Scope**: Inner functions can read variables defined in the outer function.

---

### 🏦 2. ATM Simulation Example

To demonstrate nested functions, we implemented an ATM simulation program. In this example, the main function `atm()` contains three nested functions:
- `validateUser`: Validates the PIN entered by the user.
- `showBalance`: Displays the current balance.
- `withdraw`: Validates the withdrawal amount and prints the transaction status.

#### 📝 Python Code ([day_09.py](file:///c:/Users/vijay/Desktop/pythonCourse/week_02/day_09.py))
```python
def atm():
  balance = 1000

  def validateUser(pin : int) -> bool:
    """Check whether pin is correct."""
    correct_pin = 2005

    if pin == correct_pin:
      return True
    else:
      return False

  def showBalance(balance : int) -> None:
    """Display current balance of the user."""
    print(f"Current Balance: {balance}")

  def withdraw(amount : int, balance : int) -> None:
    """Perform the withdraw operation"""
    if amount < 0:
      print("Amount cannot be negative.")
      return

    if amount > balance:
      print("Not enough funds.")
      return

    print("Please collect your cash.")
    balance -= amount
    showBalance(balance)

  pin = int(input("Enter your PIN: "))
  status = validateUser(pin)
  if status is False:
    print("PIN incorrect. Please try again.")
    return

  print("Authentication completed.")
  showBalance(balance)

  amount = int(input("Please enter amount greater than 0: "))
  withdraw(amount, balance)

atm()
```

#### 💡 Scope & Design Considerations:
- **Encapsulation**: The helper functions `validateUser`, `showBalance`, and `withdraw` are defined inside `atm()`, preventing them from polluting the global namespace.
- **Parameters**: `balance` is passed directly to `showBalance` and `withdraw` as an argument. Since integers are immutable in Python, assigning a new value to `balance` inside `withdraw` (via `balance -= amount`) only changes it inside the local scope of `withdraw`. It does not modify the `balance` variable in the outer `atm()` function. If we needed to modify the outer scope variable directly without passing parameters, we could use the `nonlocal` keyword.

---

## 📅 Day 10: Recursion & Factorial Example

On Day 10, we covered **recursion**, including the concepts of a base case, recursive case, execution flow, the call stack, and analyzed a simple recursive [factorial](file:///c:/Users/vijay/Desktop/pythonCourse/week_02/day_10.py#L9-L14) function.

### 🔄 1. What is Recursion?

**Recursion** is a programming method where a function calls itself, either directly or indirectly, to solve a problem by dividing it into smaller subproblems of the same type.

A proper recursive function contains two essential components:
- **Base Case**: The termination condition under which the function stops calling itself and starts returning values. This prevents infinite recursion and stack overflow errors (`RecursionError` in Python).
- **Recursive Case**: The code block where the function makes a recursive call to itself with a modified, usually smaller or simpler input, progressing toward the base case.

---

### 📥 2. The Recursive Stack & Flow

When a recursive function is called, Python allocates a new frame on the **call stack** to manage its execution context (local variables, arguments, and return address).

1. **Winding (Pushing)**: The function continuously calls itself, pushing a new frame onto the stack for each call, until the base case is met.
2. **Unwinding (Popping)**: Upon hitting the base case, the function starts returning values. The stack frames are popped one by one, resolving the pending computations in reverse order until the original function call completes.

#### 📊 Recursive Stack Flow for `factorial(5)`:
```
factorial(5)  -> waits for factorial(4)
  factorial(4)  -> waits for factorial(3)
    factorial(3)  -> waits for factorial(2)
      factorial(2)  -> waits for factorial(1)
        factorial(1) -> returns 1 (Base Case reached)
      factorial(2)  -> returns 2 * 1 = 2
    factorial(3)  -> returns 3 * 2 = 6
  factorial(4)  -> returns 4 * 6 = 24
factorial(5)  -> returns 5 * 24 = 120
```

---

### 💡 3. Simple Factorial Recursive Example

A classic example of recursion is computing the factorial of a number $n$ (written as $n!$).

- **Mathematical Definition**: $n! = n \times (n-1)!$ for $n > 1$, and $1! = 1$ (the base case).

#### 📝 Python Code ([day_10.py](file:///c:/Users/vijay/Desktop/pythonCourse/week_02/day_10.py))

```python
# iteration
# n = 5
# pdt = 1
# for i in range(1,n+1):
#   pdt *= i
# print(pdt)

# recursion
def factorial(n):
  # base case - ends the recursion
  if n == 1:
    return 1
  # recursive case
  return n * factorial(n-1)

print(factorial(5))
```

