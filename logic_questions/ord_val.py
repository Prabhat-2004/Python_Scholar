#Lower to upper
text = "ram"
for x in text:
    ord_val = ord(x)
    chr_val = chr(ord_val - 32)
    print(chr_val,end="")


print()

#Upper to lower
text_2 = "RAM"
for i in text_2:
    ord_val = ord(i)
    chr_val = chr(ord_val + 32)
    print(chr_val,end="")