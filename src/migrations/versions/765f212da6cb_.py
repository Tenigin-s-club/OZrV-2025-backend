"""empty message

Revision ID: 765f212da6cb
Revises: 05f9618c37b1
Create Date: 2025-04-19 02:14:39.784550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '765f212da6cb'
down_revision: Union[str, None] = '05f9618c37b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('chat_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'message', 'chat', ['chat_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_column('message', 'chat_id')
    # ### end Alembic commands ###
