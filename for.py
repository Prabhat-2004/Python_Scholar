'''for i in range(100,0,-1):
    print(i)'''
'''n = 12
for i in range(1,n-1):
    if n % i== 0:
        print(i)
    '''

'''n = int(input())
factorial = 1

for i in range (1,n+1):
    factorial = factorial * i
print(factorial)'''

"""n = 5
if n >1:
    for i in range(2,n):
        if n%i == 0:
            print("Not Prime")
    else:
        print("Prime")"""
'''
n = 7
for i in range (1, 11):
    print(i * n)'''


n = input("Enter a binary number: ")
sum = 0
power = 0
for i in range(n):
    digit = n%10
    x = x+ 2**i
    if x == n:
        print(x)