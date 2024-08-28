import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
print('Connection established')
c.execute("SELECT * FROM api_suite")
rows = c.fetchall()

for row in rows:
    print(row)



c.execute("UPDATE api_suite SET name='逻辑错误测试' WHERE id=1")
c.execute("UPDATE api_suite SET name='事实错误测试' WHERE id=2")
c.execute("UPDATE api_suite SET name='偏见与歧视测试' WHERE id=3")

conn.commit()

print('Total number of rows updated: ', conn.total_changes)

conn.close()

