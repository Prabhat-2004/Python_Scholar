strr = input("Enter Your String:").lower()
vowel = 'aeiou'
count = 0
for i in strr:
    if i in vowel:
        count += 1
    else:
        pass
print(count)