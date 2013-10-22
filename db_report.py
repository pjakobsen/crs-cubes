import sqlite3
connection = sqlite3.connect('data.sqlite')
cursor = connection.execute('select * from oecd_crs')

names = list(map(lambda x: x[0], cursor.description))

print names

cursor.execute('SELECT * FROM oecd_crs WHERE id=3011')
print cursor.fetchone()