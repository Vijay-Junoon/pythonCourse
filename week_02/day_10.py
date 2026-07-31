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
