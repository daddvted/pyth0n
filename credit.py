

total = 172000
month = 36
rate = 0.21
capital_per_month = total / month
fee = (total * rate) / 100




print(f'贷款总额: {total}')
print(f'分期数: {month}')
print(f'每期费率: {rate}')
print(f'每月归还本金: {capital_per_month}')
print(f'每期手续费: {fee}')

print('==========================')
year_rate_list = []
for n in range(1, month+1):
    year_rate = fee / total * 12
    year_rate_list.append(year_rate)
    print(f'No.{n}: {year_rate * 100:.2f}%')
    total -= capital_per_month


print(f'实际年化：{sum(year_rate_list)/len(year_rate_list)*100:.2f}%')


