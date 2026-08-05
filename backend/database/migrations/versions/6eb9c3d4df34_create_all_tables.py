"""create all tables

Revision ID: 6eb9c3d4df34
Revises: 
Create Date: 2026-07-30 16:29:58.099694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6eb9c3d4df34'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('departments',
    sa.Column('departement_id', sa.Integer(), nullable=False),
    sa.Column('departement_code', sa.String(length=20), nullable=False),
    sa.Column('departement_name', sa.String(length=100), nullable=False),
    sa.Column('departement_status', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('departement_id')
    )
    op.create_table('products',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_code', sa.String(length=20), nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=False),
    sa.Column('product_desc', sa.String(length=255), nullable=True),
    sa.Column('product_price', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('product_status', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('role', sa.Enum('employee', 'manager', 'admin', name='role_enum'), nullable=False),
    sa.Column('departement_id', sa.Integer(), nullable=False),
    sa.Column('user_status', sa.Enum('active', 'off', name='user_status_enum'), nullable=False),
    sa.ForeignKeyConstraint(['departement_id'], ['departments.departement_id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('requests',
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('request_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('approved_by', sa.Integer(), nullable=True),
    sa.Column('approved_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['approved_by'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('request_id')
    )
    op.create_table('request_detail',
    sa.Column('detail_id', sa.Integer(), nullable=False),
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.ForeignKeyConstraint(['request_id'], ['requests.request_id'], ),
    sa.PrimaryKeyConstraint('detail_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('request_detail')
    op.drop_table('requests')
    op.drop_table('users')
    op.drop_table('products')
    op.drop_table('departments')
