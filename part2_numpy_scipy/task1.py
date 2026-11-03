import numpy as np

payments = np.array([3200, 3100, 2600, 1900, 1500, 1300, 1250, 1400, 1800, 2300, 2900, 3500])

winter = payments[[11, 0, 1]]
summer = payments[[5, 6, 7]]

winter_sum = np.sum(winter)
summer_sum = np.sum(summer)

print(f"Расходы: {', '.join(map(str, payments))}")
print(f"Зимой: {winter_sum}")
print(f"Летом: {summer_sum}")

if winter_sum > summer_sum:
    print("Больше тратится зимой")
elif summer_sum > winter_sum:
    print("Больше тратится летом")
else:
    print("Расходы одинаковые")

max_payments = np.max(payments)
months = np.where(payments == max_payments)[0] + 1
print(f"Максимальные расходы: {max_payments} в месяцах: {', '.join(map(str, months))}")