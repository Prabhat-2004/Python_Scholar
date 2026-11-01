password = input("Enter Your Password: ")
alpha = ""
digit = ""
special_char = ""
for i in password:
    if i.isalpha():
        alpha += i
    elif i.isdigit():
        digit += i
    else:
        special_char += i

if len(alpha)>= 3 and len(digit) >= 2 and len(special_char) == 1:
    print("Valid Password")
else:
    print("Invalid Password")