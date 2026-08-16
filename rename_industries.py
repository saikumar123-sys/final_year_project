import sqlite3

conn = sqlite3.connect("instance/carbon_credit.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE user
SET username = 'EcoSteel Pvt Ltd'
WHERE email = 'saisteels@gmail.com'
""")

cursor.execute("""
UPDATE user
SET username = 'GreenPower Industries'
WHERE email = 'pavantech@gmail.com'
""")

cursor.execute("""
UPDATE user
SET username = 'Tech Cement Ltd'
WHERE email = 'ramalganesh@gmail.com'
""")

conn.commit()
conn.close()

print("Usernames updated successfully")
