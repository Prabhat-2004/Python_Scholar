for i in range(5):
    print("* "* i)

for i in range(5):
    print("* "* (5 - i))

for i in range(5):
    print(" "* (5-i) + "* " *i)

for i in range(5):
    print(" " *i + "* " * (5-i))

print()

for i in range(7):
    for j in range(7):
        print("*",end = " ")
    print()
print()

for i in range(7):
    for j in range(7):
        if i == 0 or j == 0 or i == 6 or j == 6:
            print("*", end =" ")
        else:
            print(" ", end = " ")
    print()