import mysql.connector as mysql

#establishing the connection => should change root user psw with full implementation
conn = mysql.connect(user='root', password='74352', host='127.0.0.1')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping database if already exists.
cursor.execute("DROP database IF EXISTS WORKORDERS")

#Preparing query to create a database
sql = "CREATE database WORKORDERS"

#Creating a database
cursor.execute(sql)

#Retrieving the list of databases
print("List of databases: ")
cursor.execute("SHOW DATABASES")
print(cursor.fetchall())

#Closing the connection
conn.close()
