import asyncpg
import asyncio

PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"

async def add_task(title, description=None, priority='normal'):
    """Insert a new task into the global queue."""
    conn = await asyncpg.connect(PG_DSN)
    try:
        res = await conn.fetchval(
            "INSERT INTO tasks (title, description, priority) VALUES ($1, $2, $3) RETURNING id",
            title, description, priority
        )
        return res
    finally:
        await conn.close()

async def get_pending_tasks(limit=10):
    """Retrieve the oldest pending tasks."""
    conn = await asyncpg.connect(PG_DSN)
    try:
        rows = await conn.fetch(
            "SELECT id, title, description, priority, created_at FROM tasks WHERE status = 'pending' ORDER BY created_at ASC LIMIT $1",
            limit
        )
        return rows
    finally:
        await conn.close()

async def update_task_status(task_id, status):
    """Update task status (pending, in_progress, completed, failed)."""
    conn = await asyncpg.connect(PG_DSN)
    try:
        await conn.execute("UPDATE tasks SET status = $1, updated_at = NOW() WHERE id = $2", status, task_id)
    finally:
        await conn.close()
