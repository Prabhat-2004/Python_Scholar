password = input("Create Your Password: ")
capital = "" 
alpha = "" 
digit = "" 
special_char = "" 

for i in password:
    if i.isalpha():
        if i.isupper():
            capital +=i
        else:
            alpha +=i
    elif i.isdigit():
        digit += i
    else:
        special_char += i

if len(capital) >= 1 and len(alpha) >=7 and len(digit) >= 2 and len(special_char) == 1:
    print("Valid Password")
else:
    print("Password is invalid")