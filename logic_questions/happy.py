num = int(input("Enter Your Number: "))


while num != 1 and num != 4:
    store = 0
    while num > 0:
        store += (num%10) ** 2
        num = num // 10
    num = store

if num ==1 :
    print("Happy Number")
else:
    print("Not A Happy Number")