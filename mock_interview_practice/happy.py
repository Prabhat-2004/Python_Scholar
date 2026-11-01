num = int(input("Enter Your Number: "))

while num != 1 and num != 4:
    store = 0
    while num > 0:
        digit = num % 10
        store = store + (digit ** 2)
        num = num // 10
    num = store
if num == 1:
    print("Happy Number")
else:
    print("Not a Happy number")