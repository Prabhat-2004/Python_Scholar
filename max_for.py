profits = [200, 450, 300]
max_profit = profits[0]
for i in profits:
    if i > max_profit:
        max_profit = i
print(max_profit)