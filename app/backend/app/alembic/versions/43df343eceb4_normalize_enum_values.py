"""normalize enum values

Revision ID: 43df343eceb4
Revises: 04e9afca21aa
"""

from typing import Sequence, Union

from alembic import op


revision: str = "43df343eceb4"
down_revision: Union[str, None] = "04e9afca21aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE employeestatus RENAME VALUE 'ACTIVE' TO 'active'"
    )
    op.execute(
        "ALTER TYPE employeestatus RENAME VALUE 'ON_LEAVE' TO 'on_leave'"
    )
    op.execute(
        "ALTER TYPE employeestatus RENAME VALUE 'INACTIVE' TO 'inactive'"
    )

    op.execute(
        "ALTER TYPE userrole RENAME VALUE 'ADMIN' TO 'admin'"
    )
    op.execute(
        "ALTER TYPE userrole RENAME VALUE 'HR_MANAGER' TO 'hr_manager'"
    )
    op.execute(
        "ALTER TYPE userrole RENAME VALUE 'EMPLOYEE' TO 'employee'"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TYPE employeestatus RENAME VALUE 'active' TO 'ACTIVE'"
    )
    op.execute(
        "ALTER TYPE employeestatus RENAME VALUE 'on_leave' TO 'ON_LEAVE'"
    )
    op.execute(
        "ALTER TYPE employeestatus RENAME VALUE 'inactive' TO 'INACTIVE'"
    )

    op.execute(
        "ALTER TYPE userrole RENAME VALUE 'admin' TO 'ADMIN'"
    )
    op.execute(
        "ALTER TYPE userrole RENAME VALUE 'hr_manager' TO 'HR_MANAGER'"
    )
    op.execute(
        "ALTER TYPE userrole RENAME VALUE 'employee' TO 'EMPLOYEE'"
    )