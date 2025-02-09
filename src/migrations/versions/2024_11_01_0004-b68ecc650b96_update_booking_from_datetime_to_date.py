"""update booking from datetime to date

Revision ID: b68ecc650b96
Revises: 9b4ff2030a38
Create Date: 2024-11-01 00:04:25.246350

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b68ecc650b96"
down_revision: Union[str, None] = "9b4ff2030a38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "bookings",
        "date_from",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.Date(),
        existing_nullable=False,
    )
    op.alter_column(
        "bookings",
        "date_to",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.Date(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "bookings",
        "date_to",
        existing_type=sa.Date(),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.alter_column(
        "bookings",
        "date_from",
        existing_type=sa.Date(),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
