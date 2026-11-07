import numpy as np
while True:
    try:
        #Длины: 12 7 15 9 20 11 6 14 10 8
        # Скорости: 40 60 50 45 70 35 55 65 50 60
        lengths = np.array(list(map(float, input("Длины: ").split())))
        speeds = np.array(list(map(float, input("Скорости: ").split())))

        k = int(input("Начальный участок k = "))
        p = int(input("Конечный участок p = "))
        t = float(input("Время t = "))

        if len(lengths) == 0:
            print("Ошибка! Массивы не должны быть пустыми.")
            continue

        if len(lengths) != len(speeds):
            print("Ошибка! Количество длин и скоростей должно совпадать.")
            continue

        if (not np.all(np.isfinite(lengths)) or not np.all(np.isfinite(speeds))):
            print("Ошибка! Все значения должны быть конечными числами.")
            continue

        if np.any(lengths <= 0) or np.any(speeds <= 0):
            print("Ошибка! Длины и скорости должны быть положительными.")
            continue

        n = len(lengths)

        if k < 1 or p > n or k > p:
            print("Ошибка! Проверьте номера участков.")
            continue

        if not np.isfinite(t) or t < 0:
            print("Ошибка! Время должно быть неотрицательным числом.")
            continue

        route_lengths = lengths[k-1:p]
        route_speeds = speeds[k-1:p]

        S = np.sum(route_lengths)

        times = route_lengths / route_speeds

        T = np.sum(times)

        if t > T and not np.isclose(t, T):
            print("Ошибка! Время превышает время прохождения маршрута.")
            continue

        V = S / T

        cumulative_times = np.cumsum(times)

        if np.isclose(t, T):
            idx = len(route_lengths) - 1
            distance = route_lengths[idx]
        else:
            idx = np.searchsorted(cumulative_times, t, side='right')

            if idx == 0:
                previous_time = 0
            else:
                previous_time = cumulative_times[idx - 1]

            distance = (t - previous_time) * route_speeds[idx]

        section = k + idx

        print(f"\nS = {S:.2f} км")
        print(f"T = {T:.2f} ч")
        print(f"V = {V:.2f} км/ч")
        print(f"Через {t:g} ч автомобиль на участке {section}, в {distance:.2f} км от его начала")

        break

    except ValueError:
        print("Ошибка! Введите корректные числовые данные.")
