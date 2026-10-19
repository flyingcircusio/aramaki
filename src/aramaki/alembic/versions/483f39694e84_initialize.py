"""initialize

Revision ID: 483f39694e84
Revises:
Create Date: 2025-09-02 15:16:18.671669

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "483f39694e84"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
