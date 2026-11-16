"""check non-negative  balance and stock

Revision ID: 4e56dff4a5eb
Revises: 
Create Date: 2026-11-16 19:54:12.336494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4e56dff4a5eb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_users_balance_non_negative",
        "users",
        "balance >= 0"
    )

    op.create_check_constraint(
        "ck_products_stock_non_negative",
        "products",
        "stock >= 0"
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_users_balance_non_negative",
        "users",
        type_="check"
    )
    op.drop_constraint(
        "ck_products_stock_non_negative",
        "products",
        type_="check"
    )
