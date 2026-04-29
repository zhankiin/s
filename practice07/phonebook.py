import psycopg2
import csv


def connect():
    return psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password="Shyngys2008",
        port="5433"
    )


def insert_console():
    conn = connect()
    cur = conn.cursor()

    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Inserted!")


def insert_csv():
    conn = connect()
    cur = conn.cursor()

    file = input("CSV file name: ")

    with open(file, "r") as f:
        reader = csv.reader(f)

        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV inserted!")


def update_data():
    conn = connect()
    cur = conn.cursor()

    name = input("Whose data update: ")
    new_phone = input("New phone: ")

    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE name=%s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Updated!")


def query_filter():
    conn = connect()
    cur = conn.cursor()

    name = input("Search name: ")

    cur.execute(
        "SELECT * FROM phonebook WHERE name=%s",
        (name,)
    )

    rows = cur.fetchall()

    for r in rows:
        print(r)

    cur.close()
    conn.close()


def delete_data():
    conn = connect()
    cur = conn.cursor()

    name = input("Delete by name: ")

    cur.execute(
        "DELETE FROM phonebook WHERE name=%s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted!")


while True:
    print("\n1 Insert console")
    print("2 Insert CSV")
    print("3 Update")
    print("4 Query")
    print("5 Delete")
    print("0 Exit")

    ch = input("Choose: ")

    if ch == "1":
        insert_console()
    elif ch == "2":
        insert_csv()
    elif ch == "3":
        update_data()
    elif ch == "4":
        query_filter()
    elif ch == "5":
        delete_data()
    elif ch == "0":
        break