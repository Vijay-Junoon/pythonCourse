from model import predict
from guidance import getGuidance

age = int(input("Enter your age: "))
bmi = float(input("Enter your BMI: "))
glucose = float(input("Enter your glucose: "))
bp = int(input("Enter your BP: "))

prediction = predict(age,bmi,glucose,bp)

print(getGuidance(age,bmi,glucose,bp,prediction))