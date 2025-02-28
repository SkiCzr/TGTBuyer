balance = 1921

i = 0
while balance > 10:
    balance = balance // 10
    i += 1
balance = balance/2
bet = balance * pow(10, (i-1))
print(bet)