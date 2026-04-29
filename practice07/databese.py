import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="123",
    port="5433"
)

cur = conn.cursor()

cur.execute("SELECT * FROM phonebook")

rows = cur.fetchall()

for r in rows:
    print(r)

cur.close()
conn.close()