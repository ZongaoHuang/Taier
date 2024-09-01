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

# import sqlite3

# conn = sqlite3.connect('db.sqlite3')
# c = conn.cursor()

# # Delete halluSuite1
# c.execute("DELETE FROM api_suite WHERE name='halluSuite1'")

# # Add new suites
# new_suites = [
#     ('越狱测试', '2023-06-01 00:00:00', 'running'),
#     ('目标劫持测试', '2023-06-01 00:00:00', 'running'),
#     ('泄露测试', '2023-06-01 00:00:00', 'running'),
#     ('等效绕过测试', '2023-06-01 00:00:00', 'running')
# ]

# c.executemany("INSERT INTO api_suite (name, time, state) VALUES (?, ?, ?)", new_suites)

# conn.commit()

# print('Total number of rows updated:', conn.total_changes)

# # Verify the changes
# c.execute("SELECT * FROM api_suite")
# rows = c.fetchall()

# print("Updated suites:")
# for row in rows:
#     print(row)

# conn.close()

import sqlite3
import random

# # Connect to the database
# conn = sqlite3.connect('db.sqlite3')
# c = conn.cursor()

# # Get the IDs of the specified test suites
# suite_names = ['越狱测试', '目标劫持测试', '泄露测试', '等效绕过测试']
# c.execute("SELECT id FROM api_suite WHERE name IN ({})".format(','.join(['?']*len(suite_names))), suite_names)
# suite_ids = [row[0] for row in c.fetchall()]

# # Update the escape_rate for tests in these suites
# for suite_id in suite_ids:
#     new_escape_rate = round(random.uniform(0.85, 0.90), 2)  # Round to 2 decimal places
#     c.execute("""
#         UPDATE api_test 
#         SET escape_rate = ?
#         WHERE suite_id = ?
#     """, (new_escape_rate, suite_id))

# # Commit the changes and close the connection
# conn.commit()
# print(f"Updated escape_rate for {c.rowcount} tests.")

# conn.close()



# Connect to the database
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Check if the 'result' column exists in the api_test table
c.execute("PRAGMA table_info(api_test)")
columns = c.fetchall()
column_names = [column[1] for column in columns]

if 'result' in column_names:
    # Remove the 'result' column from the api_test table
    c.execute("ALTER TABLE api_test DROP COLUMN result")
    print("The 'result' column has been removed from the api_test table.")
else:
    print("The 'result' column does not exist in the api_test table.")

# Commit the changes and close the connection
conn.commit()
conn.close()
