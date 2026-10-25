i = 1
n = int(input("Enter Your Number: "))
r = 0
while i < n:
    r = r*10 + (n%10)
    n = n//10
print(r)