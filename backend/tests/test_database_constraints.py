import os

import psycopg
import pytest
from psycopg.errors import CheckViolation, ForeignKeyViolation


def integration_url() -> str:
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL to run PostgreSQL constraint tests")
    return url.replace("postgresql+psycopg://", "postgresql://", 1)


@pytest.mark.integration
def test_foreign_key_checks_status_and_cascades_board_deletion() -> None:
    with psycopg.connect(integration_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO boards (name) VALUES (%s) RETURNING id",
                ("Constraint Test Board",),
            )
            board_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO tasks (board_id, title) VALUES (%s, %s) RETURNING id",
                (board_id, "Constraint Test Task"),
            )
            task_id = cursor.fetchone()[0]

            with pytest.raises(ForeignKeyViolation), connection.transaction():
                cursor.execute(
                    "INSERT INTO tasks (board_id, title) VALUES (%s, %s)",
                    (9_999_999_999, "Orphan Task"),
                )

            with pytest.raises(CheckViolation), connection.transaction():
                cursor.execute(
                    "UPDATE tasks SET status = %s WHERE id = %s",
                    ("BLOCKED", task_id),
                )

            cursor.execute("DELETE FROM boards WHERE id = %s", (board_id,))
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE id = %s", (task_id,))
            assert cursor.fetchone()[0] == 0

