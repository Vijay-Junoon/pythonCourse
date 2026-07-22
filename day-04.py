
# nums = list()
# print(nums)
# Append
# nums.append(1)
# nums.append(2)
# nums.append(3)
# nums.append([4,5,6])
# print(nums)

# Deleting Values
# 1)Pop: 
# nums.pop()
# print(nums)
# 2)Remove:
# nums.remove([4,5,6])
# print(nums)

# Inserting
# nums.insert(1,4)
# print(nums)

# Sorting
# nums = [1,6,2,5,3,4]
# nums.sort()
# print(nums)
# nums.sort(reverse = True)
# print(nums)

# Reversing the list
# nums = [1,5,2,4,3]
# nums = nums[::-1]
# print(nums)

# Sum of the list
# num = [1,2,3]
# ans = sum(num)
# print(ans)

# n = int(input("Enter n: "))
# parent = []


# for chance in range(0,n):
#   element = int(input("Enter element: "))
#   parent.append(element)
# print(parent)
parent = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even,odd = [],[]

for num in parent:
  if num%2 == 0:
    even.append(num)
  else:
    odd.append(num)

print("Even array: ",*even)
print(f"Odd: {odd}")
