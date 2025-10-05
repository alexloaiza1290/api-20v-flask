import sqlite3

connection = sqlite3.connect("database.db")

with open("api_20v_flask/schema.sql") as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

print("Base de datos inicializada correctamente.")
