"""empty message

Revision ID: 5cc6cabb8aaa
Revises: afff89d077e6
Create Date: 2025-04-18 19:43:14.205593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.config import settings
from src.parse_to_db import parse_to_db

# revision identifiers, used by Alembic.
revision: str = '5cc6cabb8aaa'
down_revision: Union[str, None] = 'afff89d077e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    parse_to_db(settings.POSTGRES_URL.replace('asyncpg', 'psycopg'))


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('TRUNCATE question_answer CASCADE;')
