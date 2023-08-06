import sqlite3
conn = sqlite3.connect('Qwe390snnskeyy46snckalkjdn872209102.db')
c = conn.cursor()
# c.execute("""CREATE TABLE stock (
#             stockid INTEGER,
#             productcode TEXT,
#             description TEXT,
#             quantity INTEGER,
#             stockindate TEXT)""")

conn.commit()
params = (1, "P0001", 'Printing Paper', 10, "leo")

c.execute("INSERT INTO stock VALUES (?, ?, ?, ?, ?)", params)
conn.commit()
conn.close()
