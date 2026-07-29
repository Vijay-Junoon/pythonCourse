
# Palindrome Checking
# def palindromeChecker(word):
#   if word == word[::-1]:
#     return True
#   return False

# userInput = input("Enter a word: ")
# if palindromeChecker(userInput):
#   print("Yes it's a palindrome")
# else:
#   print("No it's not a palindrome")


# Factorial
def computeFactorial(n):

  if n < 0:
    return ("Please enter a value greater than or equal to 0")
  fact = 1
  for i in range(1,n+1):
    fact *= i

  return fact

n = int(input("Enter a number: "))
print(f"Factorial of {n} is: {computeFactorial(n)}")