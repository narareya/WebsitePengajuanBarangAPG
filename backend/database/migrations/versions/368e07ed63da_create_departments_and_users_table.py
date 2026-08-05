from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '368e07ed63da'
down_revision: Union[str, Sequence[str], None] = '6eb9c3d4df34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(op.f('ix_departements_departement_id'), 'departments', ['departement_id'], unique=False)
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('employee', 'manager', 'admin', name='role_enum'),
               type_=sa.String(length=20),
               existing_nullable=False)
    op.alter_column('users', 'user_status',
               existing_type=postgresql.ENUM('active', 'off', name='user_status_enum'),
               type_=sa.String(length=20),
               existing_nullable=False)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.alter_column('users', 'user_status',
               existing_type=sa.String(length=20),
               type_=postgresql.ENUM('active', 'off', name='user_status_enum'),
               existing_nullable=False)
    op.alter_column('users', 'role',
               existing_type=sa.String(length=20),
               type_=postgresql.ENUM('employee', 'manager', 'admin', name='role_enum'),
               existing_nullable=False)
    op.drop_index(op.f('ix_departements_departement_id'), table_name='departments')