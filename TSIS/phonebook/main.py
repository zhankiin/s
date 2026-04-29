from services.contacts import add_contact
from services.phones import add_phone
from services.filters import filter_group, search, sort_contacts
from services.pagination import paginate
from services.json_io import export_json, import_json
from services.delete import delete_contact
from db import cur, conn

def menu():
    while True:
        print("""
1 Add Contact
2 Add Phone
3 Filter by Group
4 Search
5 Sort
6 Pagination
7 Export JSON
8 Import JSON
9 Delete Contact
0 Exit
""")

        ch = input("Choose: ")

        if ch == "1":
            add_contact()
        elif ch == "2":
            add_phone()
        elif ch == "3":
            filter_group()
        elif ch == "4":
            search()
        elif ch == "5":
            sort_contacts()
        elif ch == "6":
            paginate()
        elif ch == "7":
            export_json()
        elif ch == "8":
            import_json()
        elif ch == "9":
            delete_contact()
        elif ch == "0":
            break
        else:
            print("Wrong choice")

menu()

cur.close()
conn.close()