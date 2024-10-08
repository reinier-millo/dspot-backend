"""Add created_at and updated_at fields

Revision ID: 6102d8fec8f8
Revises: 4fa351055522
Create Date: 2024-09-08 18:02:30.987828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6102d8fec8f8'
down_revision: Union[str, None] = '4fa351055522'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friendship', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.create_index(op.f('ix_friendship_created_at'), 'friendship', ['created_at'], unique=False)
    op.add_column('profiles', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('profiles', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.create_index(op.f('ix_profiles_created_at'), 'profiles', ['created_at'], unique=False)
    op.create_index(op.f('ix_profiles_updated_at'), 'profiles', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_profiles_updated_at'), table_name='profiles')
    op.drop_index(op.f('ix_profiles_created_at'), table_name='profiles')
    op.drop_column('profiles', 'updated_at')
    op.drop_column('profiles', 'created_at')
    op.drop_index(op.f('ix_friendship_created_at'), table_name='friendship')
    op.drop_column('friendship', 'created_at')
    # ### end Alembic commands ###
