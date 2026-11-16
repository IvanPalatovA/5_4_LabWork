"""Дано: атомарный create_order уровня вашего ДЗ.
Одна транзакция, откат при сбое — против СБОЯ он корректен.
Против КОНКУРЕНЦИИ — нет. Это вы и исследуете. Правите только этот файл.
"""
from sqlalchemy import select, update
from models import User, Product, Order


class OutOfStockError(Exception): pass


class InsufficientFundsError(Exception): pass


def create_order(session, user_id, product_id):
    with session.begin():
        # user = session.get(User, user_id) # было
        user = session.execute(
            select(User).where(User.id == user_id).with_for_update()
        ).scalar_one_or_none()  # 2 задание
        if user is None:
            raise LookupError("Пользователь не найден")
        # product = session.get(Product, product_id) # было
        product = session.execute(
            select(Product).where(Product.id == product_id).with_for_update()
        ).scalar_one_or_none()  # 2 задание
        if product is None:
            raise LookupError("Товар не найден")
        price = product.price
        if product.stock <= 0:
            raise OutOfStockError("Товара нет в наличии")
        if user.balance < price:
            raise InsufficientFundsError("Недостаточно средств")
        user.balance -= price
        product.stock -= 1
        session.add(
            Order(user_id=user_id, product_id=product_id, amount=price))

# 3 задание
# def create_order(session, user_id, product_id):
#     with session.begin():
#         stock_res = session.execute(
#             update(Product)
#             .where(Product.id == product_id, Product.stock > 0)
#             .values(stock=Product.stock - 1)
#         )
#         if stock_res.rowcount == 0:
#             exists = session.get(Product, product_id)
#             if exists is None:
#                 raise LookupError("Товар не найден")
#             raise OutOfStockError("Товара нет в наличии")
#
#         product = session.get(Product, product_id)
#
#         bal_res = session.execute(
#             update(User)
#             .where(User.id == user_id, User.balance >= product.price)
#             .values(balance=User.balance - product.price)
#         )
#         if bal_res.rowcount == 0:
#             if session.get(User, user_id) is None:
#                 raise LookupError("Пользователь не найден")
#             raise InsufficientFundsError("Недостаточно средств")
#
#         session.add(Order(user_id=user_id, product_id=product_id, amount=product.price))
