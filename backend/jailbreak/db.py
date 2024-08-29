# import sqlite3

# conn = sqlite3.connect('db.sqlite3')
# c = conn.cursor()
# print('Connection established')
# c.execute("SELECT * FROM api_suite")
# rows = c.fetchall()

# for row in rows:
#     print(row)



# c.execute("UPDATE api_suite SET name='逻辑错误测试' WHERE id=1")
# c.execute("UPDATE api_suite SET name='事实错误测试' WHERE id=2")
# c.execute("UPDATE api_suite SET name='偏见与歧视测试' WHERE id=3")

# conn.commit()

# print('Total number of rows updated: ', conn.total_changes)

# conn.close()

import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Delete halluSuite1
c.execute("DELETE FROM api_suite WHERE name='halluSuite1'")

# Add new suites
new_suites = [
    ('越狱测试', '2023-06-01 00:00:00', 'running'),
    ('目标劫持测试', '2023-06-01 00:00:00', 'running'),
    ('泄露测试', '2023-06-01 00:00:00', 'running'),
    ('等效绕过测试', '2023-06-01 00:00:00', 'running')
]

c.executemany("INSERT INTO api_suite (name, time, state) VALUES (?, ?, ?)", new_suites)

conn.commit()

print('Total number of rows updated:', conn.total_changes)

# Verify the changes
c.execute("SELECT * FROM api_suite")
rows = c.fetchall()

print("Updated suites:")
for row in rows:
    print(row)

conn.close()
