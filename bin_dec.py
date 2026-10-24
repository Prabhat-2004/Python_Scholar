num = 1011
decimal = 0
power = 0
   

while num > 0:
    digit = num % 10
    decimal = decimal + digit * (2**power)
    num = num // 10
    power += 1

print(decimal)


