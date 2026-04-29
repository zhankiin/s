from db import cur

def get_group_id(group_name):
    group_name = group_name or "default"

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    result = cur.fetchone()

    if result:
        return result[0]

    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) RETURNING id",
        (group_name,)
    )
    return cur.fetchone()[0]