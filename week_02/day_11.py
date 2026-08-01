
def add(n,m):
  # ! base case
  if m == n:
    return n
  return m + add(n,m-1)

n = int(input("Enter first number: "))
m = int(input("Enter second number: "))

print(add(n,m))