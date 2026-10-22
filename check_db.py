
import sqlite3

connection = sqlite3.connect("ecommerce.db")

query = """
SELECT name
FROM sqlite_master
WHERE type = 'table'
AND name NOT LIKE 'sqlite_%'
ORDER BY name;
"""

tables = connection.execute(query).fetchall()

print("Database tables:")

for table in tables:
    print(table[0])

connection.close()
