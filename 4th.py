'''cpu_hours = int(input("Enter number of cpu hours:"))
storage = int(input("Enter storage in gb:"))
data_transfer = int(input("Enter data transfer in gb:"))
cpu_cost = cpu_hours * 5
storage_cost = storage * 2
data_transfer_cost = data_transfer * 1
total_amount = cpu_cost + storage_cost + data_transfer_cost
if cpu_hours > 100:
    print(total_amount+500)
else:
    print(total_amount)
'''

#if-elif_else
monthly_bill = int(input())
uptime = float(input())
refund = 0
if uptime >= 99.9 :
    print("No Refund")
elif uptime >= 98 and uptime < 99.9:
    refund = monthly_bill * 0.10
    
else:
    refund = monthly_bill*0.25

print("Refund Amount:", refund)