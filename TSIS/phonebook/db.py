import psycopg2

conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)

cur = conn.cursor()