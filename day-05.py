
# d1['key'] = value


# d1['s_id'] = 100
# d1['name'] = "Ajay"
# d1['marks'] = [1,2,3]
# d1['contact'] = {'dad' : 1234567890, "mom": 9876542312}
# print(d1)

# Anagram or not
w1 = input("Enter word 1: ")
w2 = input("Enter word 2: ")
d1 = {}
d2 = {}
print("---Populating---")
for ch in w1:
  d1[ch] = d1.get(ch,0) + 1

print("---Populating---")
for ch in w2:
  d2[ch] = d2.get(ch,0) + 1

if d1 == d2:
  print("Anagram")
else:
  print("Not Anagram")
