n = int(input("Enter Your Number:"))
while n != 1 and n != 4:
    happy = 0
    while n>0:
        digit = n%10
        happy = happy + digit * digit
        n = n//10
    n = happy

if n == 1:
    print("Happy Number")
else:
    print("Not a happy number")