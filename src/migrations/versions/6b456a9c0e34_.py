"""empty message

Revision ID: 6b456a9c0e34
Revises: 7ec1ea7aa7c1
Create Date: 2025-04-18 23:10:57.289559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.config import settings
from src.parse_to_db import parse_to_db

# revision identifiers, used by Alembic.
revision: str = '6b456a9c0e34'
down_revision: Union[str, None] = '7ec1ea7aa7c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()
    parse_to_db(settings.POSTGRES_URL.replace('asyncpg', 'psycopg'))


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('TRUNCATE question_answers CASCADE;')
