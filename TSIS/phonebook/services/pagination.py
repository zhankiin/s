from db import cur

def paginate():
    limit = 3
    offset = 0

    while True:
        cur.execute("""
            SELECT c.name, p.phone, c.email
            FROM contacts c
            LEFT JOIN phones p ON p.contact_id = c.id
            ORDER BY c.id
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        if not rows:
            print("No more data")
            break

        for row in rows:
            print(row)

        cmd = input("next / prev / quit: ").lower()

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break
        