from db import cur, conn
from services.groups import get_group_id

def add_contact():
    # Ввод данных пользователя
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")

    # Получаем ID группы (или создаём новую, если её нет)
    gid = get_group_id(group_name)

    # Проверяем, существует ли контакт с таким именем
    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    existing = cur.fetchone()

    # Если контакт уже есть
    if existing:
        # Спрашиваем, перезаписать ли данные
        choice = input("Contact exists. overwrite? (yes/no): ")

        # Если пользователь отказался — выходим
        if choice.lower() != "yes":
            print("Skipped")
            return

        # Берём ID существующего контакта
        contact_id = existing[0]

        # Обновляем данные контакта (email, дата рождения, группа)
        cur.execute("""
            UPDATE contacts
            SET email = %s, birthday = %s, group_id = %s
            WHERE id = %s
        """, (email, birthday, gid, contact_id))

        # Удаляем старые телефоны контакта
        cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

        # Добавляем новый телефон
        cur.execute(
            "INSERT INTO phones(contact_id, phone) VALUES (%s, %s)",
            (contact_id, phone)
        )

    else:
        # Если контакт новый — создаём запись
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, gid))

        # Получаем ID только что созданного контакта
        contact_id = cur.fetchone()[0]

        # Добавляем телефон к новому контакту
        cur.execute(
            "INSERT INTO phones(contact_id, phone) VALUES (%s, %s)",
            (contact_id, phone)
        )

    # Сохраняем изменения в базе данных
    conn.commit()

    # Сообщаем пользователю об успешной операции
    print("Done!")