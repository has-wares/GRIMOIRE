import sqlite3
from datetime import datetime

def init_db(conn):
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS grim(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            content TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)


        #VIRTUAL TABLE
        conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS grim_search USING fts5(
        name,
        tags,
        content,
        content='grim',
        content_rowid='id'
        )
        """)

        #TRIGGERS
        conn.execute("""
        CREATE TRIGGER IF NOT EXISTS grim_ai AFTER INSERT ON grim
        BEGIN INSERT INTO grim_search(rowid, name, tags, content)
        VALUES (new.id, new.name, new.tags, new.content); END;
        """)
        conn.execute("""
        CREATE TRIGGER IF NOT EXISTS grim_ad AFTER DELETE ON grim
        BEGIN INSERT INTO grim_search(grim_search, rowid, name, tags, content)
        VALUES('delete', old.id, old.name, old.tags, old.content); END;
        """)
        conn.execute("""
        CREATE TRIGGER IF NOT EXISTS grim_au
        AFTER UPDATE ON grim BEGIN INSERT INTO grim_search(grim_search, rowid, name, tags, content)
        VALUES('delete', old.id, old.name, old.tags, old.content); INSERT INTO grim_search(rowid, name, tags, content)
        VALUES (new.id, new.name, new.tags, new.content); END;
        """)

def make_note(conn, name, content, tags):
    query = "INSERT INTO grim (name, content, tags) VALUES (?,?,?)"
    with conn:
        conn.execute(query, (name, content, tags))

def get_byname(conn, name):
    cursor = conn.execute("SELECT content FROM grim WHERE name = ?", (name,))
    row = cursor.fetchone()
    return row[0] if row else None

def get_byid(conn, num):
    cursor = conn.execute("SELECT content FROM grim WHERE id = ?", (num,))
    row = cursor.fetchone()
    return row[0] if row else None

def get_namebyid(conn, num):
    cursor = conn.execute("SELECT name FROM grim WHERE id = ?", (num,))
    row = cursor.fetchone()
    return row[0] if row else None

def get_id_byname(conn, name):
    row = conn.execute(
        "SELECT id FROM grim WHERE LOWER(name)=LOWER(?)",
        (name,)
    ).fetchone()
    return row[0] if row else None

def update_byname(conn, name, new_cont):
    query = """UPDATE grim SET content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE name = ?"""
    with conn:
        conn.execute(query, (new_cont, name))

def update_byid(conn, num, new_cont):
    query = """UPDATE grim SET content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?"""
    with conn:
        conn.execute(query, (new_cont, num))


def listemall(conn):
    cursor = conn.execute("""
            SELECT id, name, tags, created_at
            FROM grim ORDER BY created_at
            """)
    return cursor.fetchall()
    
def listemnew(conn):
    cursor = conn.execute("""
            SELECT id, name, tags, updated_at
            FROM grim ORDER BY updated_at DESC
            """)
    return cursor.fetchall()


def list_bytag(conn, tags):
    where_clause = ["LOWER(tags) LIKE ?" for _ in tags]
    query = f"""
            SELECT id, name, tags, created_at
            FROM grim WHERE {' OR '.join(where_clause)}
            ORDER BY created_at
            """
    params = [f"%{t}%" for t in tags]
    cursor = conn.execute(query, params)
    return cursor.fetchall()

def list_bytag_n(conn, tags):
    where_clause = ["LOWER(tags) LIKE ?" for _ in tags]
    query = f"""
            SELECT id, name, tags, updated_at
            FROM grim WHERE {' OR '.join(where_clause)}
            ORDER BY updated_at DESC
            """
    params = [f"%{t}%" for t in tags]
    cursor = conn.execute(query, params)
    return cursor.fetchall()

def list_exact(conn, tags):
    tags = ','.join(tags) if isinstance(tags, list) else tags
    query = """
            SELECT id, name, tags, created_at
            FROM grim WHERE LOWER(tags) = ?
            ORDER BY created_at
            """
    cursor = conn.execute(query, (tags.lower(),))
    return cursor.fetchall()

def list_exact_new(conn, tags):
    tags = ','.join(tags) if isinstance(tags, list) else tags
    query = """
            SELECT id, name, tags, created_at
            FROM grim WHERE LOWER(tags) = ?
            ORDER BY updated_at DESC
            """
    cursor = conn.execute(query, (tags.lower(),))
    return cursor.fetchall()

    
def remove_byname(conn, name):
    query = "DELETE FROM grim WHERE name = ?"
    with conn:
        cursor = conn.execute(query, (name,))
        return cursor.rowcount > 0

def remove_byid(conn, num):
    query = "DELETE FROM grim WHERE id = ?"
    with conn:
        cursor = conn.execute(query, (num,))
        return cursor.rowcount > 0

def retag_byname(conn, name, new_tags):
    query = """UPDATE grim SET tags = ?,
               updated_at = CURRENT_TIMESTAMP
               WHERE name = ? """
    with conn:
        conn.execute(query, (new_tags, name))

def retag_byid(conn, num, new_tags):
    query = """UPDATE grim SET tags = ?,
               updated_at = CURRENT_TIMESTAMP
               WHERE id = ? """
    with conn:
        conn.execute(query, (new_tags, num))
        



def rename_byname(conn, name, new_name):
    query = """
            UPDATE grim
            SET name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE name = ?
            """
    with conn:
        conn.execute(query, (new_name, name))

def rename_byid(conn, num, new_name):
    query = """
            UPDATE grim
            SET name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """
    with conn:
        conn.execute(query, (new_name, num))

def search(conn, query):
    sql = """
        SELECT b.id, b.name, b.tags, b.updated_at
        FROM grim b
        JOIN grim_search s ON b.id = s.rowid
        WHERE grim_search MATCH ?
        ORDER BY rank
    """

    try:
        cursor = conn.execute(sql, (query,))
        return cursor.fetchall()
    except sqlite3.OperationalError:
        return None
