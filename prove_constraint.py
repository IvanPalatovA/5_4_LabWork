from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from models import User, Product


def try_violation(label, fn):
    try:
        fn()
        print(f"[FAIL] {label}: БД ПРОПУСТИЛА невозможное состояние!")
    except IntegrityError as e:
        print(f"[OK]   {label}: БД отклонила -> {e.orig.__class__.__name__}")


def main():
    with SessionLocal.begin() as s:
        s.get(User, 1).balance = Decimal("100.00")
        s.get(Product, 1).stock = 1

    def neg_balance():
        with SessionLocal.begin() as s:
            s.execute(
                text("UPDATE users SET balance = balance - 9999 WHERE id = 1"))

    def neg_stock():
        with SessionLocal.begin() as s:
            s.execute(
                text("UPDATE products SET stock = stock - 5 WHERE id = 1"))

    try_violation("balance >= 0", neg_balance)
    try_violation("stock   >= 0", neg_stock)

    with SessionLocal() as s:
        b = s.get(User, 1).balance
        st = s.get(Product, 1).stock
    print(
        f"После попыток: balance={b}, stock={st} (должны остаться 100.00 и 1)")


if __name__ == "__main__":
    main()
