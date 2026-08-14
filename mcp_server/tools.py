from db import get_connection


def get_users(limit: int = 5):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id,
               first_name,
               last_name,
               email
        FROM users
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "first_name": r[1],
            "last_name": r[2],
            "email": r[3]
        }
        for r in rows
    ]


def get_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id,
               first_name,
               last_name,
               email
        FROM users
        WHERE id=%s
    """, (user_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return {"error": "User not found"}

    return {
        "id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "email": row[3]
    }


def search_users(name: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id,
               first_name,
               last_name,
               email
        FROM users
        WHERE first_name ILIKE %s
           OR last_name ILIKE %s
    """, (f"%{name}%", f"%{name}%"))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "first_name": r[1],
            "last_name": r[2],
            "email": r[3]
        }
        for r in rows
    ]
