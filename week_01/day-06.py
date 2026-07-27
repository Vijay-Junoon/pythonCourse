# 1st Question
numbers = [4, -2, 0, 7, -5, 0, 9, -1]
pos,neg,zero = 0,0,0
for num in numbers:
  if num > 0: pos += 1
  elif num < 0: neg += 1
  else: zero += 1

print(f"Positive: {pos}")
print(f"Negative: {neg}")
print(f"Zero: {zero}")

# 2nd Question
words = ["apple", "banana", "apple", "orange", "banana", "apple"]

freq = {}

for word in words:
  freq[word] = freq.get(word,0) + 1

for k,v in freq.items():
  print(f"{k} : {v}")


# 3rd Question
marks = {
"Alice": 90,
"Bob": 65,
"Charlie": 82,
"David": 45
}

results = {}

for student in marks:
  if marks[student] > 50:
    results[student] = "Passed"
  else:
    results[student] = "Failed"

for student,status in results.items():
  print(f"{student} : {status}") 


# 4th Question
cart = {
"Milk": 40,
"Bread": 30,
"Eggs": 60,
"Butter": 80
}

total_amount = 0
for product,price in cart.items():
  total_amount += price
print(f"Total Bill: {total_amount}")
if total_amount > 150:
  print("Discount Applied")
else:
  print("No Discount")