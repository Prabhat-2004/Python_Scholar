sentence = input("Enter a sentence or Word: ")
vowel = 'aeiou'
count_vowel = 0
for i in sentence:
    if i in vowel:
        count_vowel += 1
    else:
        pass
print(count_vowel)

