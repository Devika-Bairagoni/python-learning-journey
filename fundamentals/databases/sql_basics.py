import sqlite3
from pathlib import Path

DB_PATH = Path("fundamentals/databases/basics_demo.db")

print("=== Creating a Database and Table ===")

# connect() creates the file if it does not exist
# Using context manager ensures connection closes cleanly
with sqlite3.connect(DB_PATH) as conn:
    # cursor executes SQL statements
    cursor = conn.cursor()

    # CREATE TABLE IF NOT EXISTS prevents error if table already exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL UNIQUE,
            region      TEXT    NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'stopped',
            cpu_usage   REAL    DEFAULT 0.0,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # conn.commit() saves changes to disk
    # Without commit, changes exist only in memory
    conn.commit()
    print(f"  Database created: {DB_PATH}")
    print(f"  Table 'servers' ready.")


print("\n=== Inserting Data ===")

servers_to_add = [
    ("api-server-01", "us-east-1",  "running",  45.2),
    ("db-server-01",  "us-east-1",  "running",  78.9),
    ("cache-01",      "us-west-2",  "degraded", 91.3),
    ("api-server-02", "us-west-2",  "stopped",   0.0),
]

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    # executemany inserts multiple rows efficiently
    # ? placeholders prevent SQL injection — ALWAYS use placeholders
    cursor.executemany("""
        INSERT OR IGNORE INTO servers (name, region, status, cpu_usage)
        VALUES (?, ?, ?, ?)
    """, servers_to_add)

    conn.commit()
    print(f"  Inserted {cursor.rowcount} rows.")


print("\n=== Selecting Data ===")

with sqlite3.connect(DB_PATH) as conn:
    # row_factory makes rows behave like dicts
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Select all rows
    cursor.execute("SELECT * FROM servers ORDER BY id")
    rows = cursor.fetchall()

    print(f"  Total servers: {len(rows)}")
    for row in rows:
        print(f"  [{row['id']}] {row['name']} | {row['region']} | {row['status']}")


print("\n=== Filtering with WHERE ===")

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # WHERE filters rows — always use ? for values, never f-strings
    cursor.execute("""
        SELECT name, cpu_usage FROM servers
        WHERE cpu_usage > ?
        ORDER BY cpu_usage DESC
    """, (80.0,))

    high_cpu = cursor.fetchall()
    print(f"  High CPU servers (> 80%):")
    for row in high_cpu:
        print(f"    {row['name']}: {row['cpu_usage']}%")


print("\n=== Updating Data ===")

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE servers SET status = ?, cpu_usage = ?
        WHERE name = ?
    """, ("running", 32.1, "api-server-02"))

    conn.commit()
    print(f"  Updated {cursor.rowcount} row(s).")


print("\n=== Aggregation Queries ===")

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*)            AS total,
            AVG(cpu_usage)      AS avg_cpu,
            MAX(cpu_usage)      AS max_cpu,
            MIN(cpu_usage)      AS min_cpu
        FROM servers
        WHERE status = 'running'
    """)

    stats = cursor.fetchone()
    print(f"  Running servers : {stats['total']}")
    print(f"  Average CPU     : {stats['avg_cpu']:.1f}%")
    print(f"  Max CPU         : {stats['max_cpu']}%")
    print(f"  Min CPU         : {stats['min_cpu']}%")


print("\n=== Deleting Data ===")

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM servers WHERE status = ?", ("stopped",))
    conn.commit()
    print(f"  Deleted {cursor.rowcount} stopped server(s).")

print("\nsql_basics.py completed successfully.")