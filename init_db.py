import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='vitalijko',
    passwd='12345678'
)

cursor = db.cursor()

cursor.execute('CREATE DATABASE age')

print('Done!')
