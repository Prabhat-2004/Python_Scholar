#PGR - 1
p = 1000
t = 1
r = 10
si = (p*t*r)//100
print(f"Simple interest amount: {si}")


#PGR -2
p = 1000
t = 2
r = 10
ci = p*(1+(r/100))**t-p
print(ci)

#PGR - 3
phy = 90
bio = 80
eng = 90
avg = (phy + bio + eng)/3
print(f"AVG: {avg}")


#pgr - 3
a = 10
b = 20
print("a:",a)
print("b:",b)
#After Swap
a,b = b,a
print("a:",a)
print("b:",b)


#TYPE Casting

num1 = int(input("ENTER NO-1:"))
num2 = int(input("ENTER NO-2:"))

print("OUT PUT:", num1 + num2)