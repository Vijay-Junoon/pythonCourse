# l1 = [0,-1,1,2,3]
# l2 = [0,-1,-2,3,5]

# def countPos(user_list):
#   pos = 0
#   for i in user_list:
#     if i > 0:
#       pos += 1
#   return pos

# pos_l1 = countPos(l1)
# pos_l2 = countPos(l2)


# if pos_l1 == pos_l2:
#   print("Same Pos Nums")
# else:
#   print("No")

# Function Definition
# def greet(text_message):
#   print(text_message)

# Function Call
# greet(54)

# def add(a,b):
#   s = a + b
#   return s

# sum1 = add(1,2)
# sum2 = add(sum1,3)

# print(sum2)

def even_odd (val):
    if val % 2 == 0:
        return f"Number {val} is even"
    else:
        return f"Number {val} is odd"

val1 = int(input("Enter the number: "))
result = even_odd(val1)
print(result)
