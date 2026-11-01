x = "PrBhAt"
for i in x:
    if ord(i)  <= 90:
        low = ord(i) + 32
        print(chr(low),end = " ")
    else:
        print(i, end = " ")

print()

for i in x:
    if ord(i) >= 97:
        cap = ord(i)- 32
        print(chr(cap),end = " ")
    else:
        print(i, end = " ")