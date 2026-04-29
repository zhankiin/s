import json
import os
from db import cur, conn
from config import JSON_FILE
from services.groups import get_group_id

def export_json():
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
    """)

    data = []

    for contact_id, name, email, birthday, group_name in cur.fetchall():
        cur.execute(
            "SELECT phone FROM phones WHERE contact_id = %s",
            (contact_id,)
        )

        phones = [row[0] for row in cur.fetchall()]

        data.append({
            "name": name,
            "phones": phones,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name
        })

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Exported!")


def import_json():
    if not os.path.exists(JSON_FILE):
        print("contacts.json not found")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for c in data:
        name = c.get("name")
        email = c.get("email")
        birthday = c.get("birthday")

        if birthday in ["None", "", None]:
            birthday = None
        group_name = c.get("group") or "default"

        if not name:
            print("Skipped contact without name")
            continue

        gid = get_group_id(group_name)

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} exists (skip/overwrite): ").lower()

            if choice == "skip":
                continue

            contact_id = existing[0]

            cur.execute("""
                UPDATE contacts
                SET email = %s, birthday = %s, group_id = %s
                WHERE id = %s
            """, (email, birthday, gid, contact_id))

            cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

        else:
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, gid))

            contact_id = cur.fetchone()[0]

        phones = c.get("phones")

        if phones is None:
            phones = [c.get("phone")]

        for phone in phones:
            if phone:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone)
                    VALUES (%s, %s)
                """, (contact_id, phone))

    conn.commit()
    print("Imported!")