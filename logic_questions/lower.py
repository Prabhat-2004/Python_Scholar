s = "HELLO"
for i in s:
    ord_val = ord(i)
    char = chr(ord_val + 32)
    print(char, end="")