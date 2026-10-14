rama = 1.3
raja = 1.7
if rama > raja:
    print("Rama is taller")
else:
    print("Raja is taller")


#Code-2
total = float(input("Enter total purchase amount:"))
if total >= 1000:
    discount = total * 0.10
    final_amount = total - discount
    print("Discount applied:", discount)
    print("Final amount to pay:", final_amount)
else:
    print("No apply discount")
    print("Total ammount:", total)