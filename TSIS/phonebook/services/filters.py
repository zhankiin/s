from db import cur

def filter_group():
    group_name = input("Group: ")

    cur.execute("""
        SELECT c.name, p.phone, c.email, c.birthday
        FROM contacts c
        LEFT JOIN phones p ON p.contact_id = c.id
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
        ORDER BY c.name
    """, (group_name,))

    rows = cur.fetchall()

    if not rows:
        print("No contacts in this group")
    else:
        for row in rows:
            print(row)


def search():
    q = input("Search: ").strip()

    cur.execute("""
        SELECT c.name, p.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN phones p ON p.contact_id = c.id
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.name ILIKE %s
           OR p.phone ILIKE %s
           OR c.email ILIKE %s
        ORDER BY c.name
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))

    rows = cur.fetchall()

    if not rows:
        print("No results")
    else:
        for row in rows:
            print(row)


def sort_contacts():
    field = input("Sort by (name/birthday/created_at): ")

    if field not in ["name", "birthday", "created_at"]:
        field = "name"

    cur.execute(f"""
        SELECT c.name, p.phone, c.email, c.birthday
        FROM contacts c
        LEFT JOIN phones p ON p.contact_id = c.id
        ORDER BY c.{field}
    """)

    for row in cur.fetchall():
        print(row)