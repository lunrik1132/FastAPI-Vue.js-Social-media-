import sqlite3

db = sqlite3.connect("blog.db")
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS posts;")
db.commit()
db.close()

print("Таблица posts удалена!")
