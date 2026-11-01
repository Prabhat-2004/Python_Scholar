password = input("Enter Your Password: ")
alpha =0
special = 0
digit = 0
capital = 0

for i in password:
    if i.isupper():
        capital += 1
    elif i.isalpha():
        alpha += 1
    elif i.isdigit():
        digit +=1
    else:
        special += 1

if capital >= 1 and alpha >= 4 and digit >= 2 and special == 1:
    print("Valid Password")
else:
    print("Invalid Password")
    