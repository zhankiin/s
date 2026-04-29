from db import cur, conn

def add_phone():
    name = input("Name: ")
    phone = input("New phone: ")

    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    result = cur.fetchone()

    if not result:
        print("Contact not found")
        return

    contact_id = result[0]

    cur.execute(
        "INSERT INTO phones(contact_id, phone) VALUES (%s, %s)",
        (contact_id, phone)
    )

    conn.commit()
    print("Phone added!")