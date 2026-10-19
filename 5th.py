'''w = float(input("Weight:"))
h = float(input("Height:"))
bmi = w/(h**2)

if bmi < 18.5:
    print("Under Wight")
elif 18.5 <= bmi and bmi < 25:
    print("Normal")
elif 25 <= bmi and bmi < 30  :
    print("Over Weight")
elif bmi >= 30:
    print("Obese")
else:
    print("Give correct input")

'''

#2nd code
'''units = int(input("Enter number units used:"))
if units <= 100:
    bill = units*1
elif units <= 200:
    bill = 100 *1 + (units-100) * 2
else:
    bill = 100 *1 + 100 * 2+ (units-200)*5
print(f"Electricity Bill: {bill} rupee")
'''

#3re code
'''a = int(input("Enter first angle:"))
b = int(input("Enter second angle:"))
c = int(input("Enter third angle:"))

if a==b and b==c and c==a:
    print("Equilateral Traingle")
elif a ==b or b==c or c==a :
    print("Isosceles Traingle")
else:
    print("Scalene Traingle")
'''

age = int(input("Enter Age:"))
if age >= 18:
    print("Allowed for match")
    if age >=18 and age < 30:
        print("$2 ticket price")
    elif age >= 30 and age < 60:
        print("$1 ticket price")
    else:
        print("Free ticket price")
else:
    print("Less than 18 age we don't allow for match")