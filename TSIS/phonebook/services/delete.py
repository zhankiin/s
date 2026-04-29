from db import cur, conn

def delete_contact():
    name = input("Enter name to delete: ")

    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    result = cur.fetchone()

    if not result:
        print("Contact not found")
        return

    contact_id = result[0]

    cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
    cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))

    conn.commit()
    print("Deleted successfully!")