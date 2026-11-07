import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd

START_DATE = "2022-01-01"
DAYS_IN_YEAR = 365
MIN_STORES = 5

CITIES = ["Минск", "Гомель", "Могилёв", "Витебск",
          "Гродно", "Брест", "Дрогичин", "Барановичи"]
PAYMENT_METHODS = ["наличные", "карта", "онлайн"]
PAYMENT_PROBS = [0.25, 0.55, 0.20]

PRODUCTS = [
    ("Напитки", "Кола", 90, 50, 40, 0.0010),
    ("Напитки", "Сок", 120, 70, 25, -0.0005),
    ("Напитки", "Вода", 50, 25, 60, 0.0003),
    ("Молочные", "Молоко", 85, 55, 50, 0.0002),
    ("Молочные", "Сыр", 450, 300, 15, 0.0008),
    ("Молочные", "Йогурт", 70, 40, 35, -0.0008),
    ("Выпечка", "Хлеб", 55, 30, 70, -0.0002),
    ("Выпечка", "Круассан", 110, 60, 20, 0.0012),
    ("Выпечка", "Пирог", 300, 170, 10, 0.0005),
]
COLUMNS = ["date", "store_id", "city", "category", "product",
           "qty", "price", "cost", "promo", "payment_method"]


class InvalidConfigError(Exception):
    """Некорректные параметры запуска."""


class OutputWriteError(Exception):
    """Не удалось записать результирующий файл."""


def validate_config(years, stores, out):
    """Проверяет параметры запуска."""
    if years <= 0 or years > 10:
        raise InvalidConfigError("--years должен быть от 1 до 10")
    if stores < MIN_STORES or stores > 50:
        raise InvalidConfigError(f"--stores должен быть от {MIN_STORES} до 50")
    if out is None or not str(out).strip():
        raise InvalidConfigError(f"--out не может быть пустым: {out!r}")


def generate_sales(seed, years, stores):
    """Генерирует таблицу посуточных продаж сети магазинов.

    Закладывает тренд, недельную и годовую сезонность, влияние акций,
    шум, выбросы (~1.5% по qty) и пропуски (~1% в price и payment_method).
    Один и тот же seed всегда даёт одну и ту же таблицу.

    :return: pandas.DataFrame со столбцами COLUMNS
    """
    rng = np.random.default_rng(seed)

    dates = pd.date_range(START_DATE, periods=years * DAYS_IN_YEAR, freq="D")
    catalog = pd.DataFrame(
        PRODUCTS,
        columns=["category", "product", "base_price", "base_cost", "base_qty", "trend"],
    )

    index = pd.MultiIndex.from_product(
        [dates, range(1, stores + 1), catalog["product"].tolist()],
        names=["date", "store_id", "product"],
    )
    df = index.to_frame(index=False).merge(catalog, on="product", how="left")
    n = len(df)

    store_ids = df["store_id"].to_numpy()
    df["city"] = np.array(CITIES)[(store_ids - 1) % len(CITIES)]
    store_factor = rng.uniform(0.7, 1.4, stores)[store_ids - 1]

    t = (df["date"] - dates[0]).dt.days.to_numpy()
    day_of_week = df["date"].dt.dayofweek.to_numpy()
    day_of_year = df["date"].dt.dayofyear.to_numpy()

    trend = np.clip(1 + df["trend"].to_numpy() * t, 0.1, None)
    weekly = np.where(day_of_week >= 5, 1.3, 1.0)
    yearly = np.where(
        df["category"].to_numpy() == "Напитки",
        1 + 0.35 * np.sin(2 * np.pi * (day_of_year - 80) / DAYS_IN_YEAR),
        1.0,
    )
    promo = (rng.random(n) < 0.15).astype(int)

    expected_qty = (df["base_qty"].to_numpy() * store_factor * trend
                    * weekly * yearly * np.where(promo == 1, 1.4, 1.0))
    qty = rng.poisson(expected_qty)

    outlier = rng.random(n) < 0.015
    qty = np.where(outlier, qty * rng.integers(5, 11, n), qty)

    price = (df["base_price"].to_numpy() * (1 + 0.0001 * t)
             * np.where(promo == 1, 0.85, 1.0) * rng.normal(1, 0.02, n)).round(2)
    cost = (df["base_cost"].to_numpy() * (1 + 0.00005 * t)).round(2)

    payment = rng.choice(PAYMENT_METHODS, size=n, p=PAYMENT_PROBS)

    price[rng.random(n) < 0.01] = np.nan
    payment = pd.Series(payment).mask(rng.random(n) < 0.01)

    df["qty"] = qty
    df["price"] = price
    df["cost"] = cost
    df["promo"] = promo
    df["payment_method"] = payment
    return df[COLUMNS]


def save_csv(df, out):
    """Сохраняет таблицу в CSV, создавая папку при необходимости."""
    path = Path(out)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False, encoding="utf-8")
    except OSError as exc:
        raise OutputWriteError(f"Не удалось записать {str(path)!r}: {exc}") from exc


def parse_args(argv=None):
    """Разбирает аргументы командной строки."""
    default_out = Path(__file__).parent / "data" / "sales.csv"
    parser = argparse.ArgumentParser(description="Генератор синтетических данных о продажах")
    parser.add_argument("--seed", type=int, default=42, help="сид генератора случайных чисел")
    parser.add_argument("--years", type=int, default=3, help="количество лет данных")
    parser.add_argument("--stores", type=int, default=5, help="количество магазинов")
    parser.add_argument("--out", default=str(default_out), help="путь к файлу")
    return parser.parse_args(argv)


def main(argv=None):
    """Главная функция: :0 при успехе, 1 при ошибке параметров или записи"""
    args = parse_args(argv)
    try:
        validate_config(args.years, args.stores, args.out)
        df = generate_sales(args.seed, args.years, args.stores)
        save_csv(df, args.out)
    except (InvalidConfigError, OutputWriteError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1
    print(f"Готово: {len(df)} строк записано в {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())