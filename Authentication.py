import hashlib
from database_connector import WorkOrdersDB
import mysql.connector
from tkinter import messagebox

db = WorkOrdersDB()

class Authenticate:
    def __init__(self):
        self.connection = None

    def hash_password(self, password):
        salt = "my_salt"
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    def authenticate(self, password):
        db.connect()
        cursor = db.connection.cursor()
        query = "SELECT password FROM users WHERE username IN ('Root', 'Users')"
        cursor.execute(query)
        results = cursor.fetchall()
        db.close()
        for result in results:
            print(result)
            if password == result[0]:
                return True
        return False

    def register(self, username, password):
        db.connect()
        cursor = db.connection.cursor()
        hashed_password = db.hash_password(password)
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        db.connection.commit()
        db.close()

    def change_password(self, old_password, new_password, confirm_password, window):
        # Check if the old password is correct
        if self.authenticate(self.hash_password(old_password)) == False:
            messagebox.showerror("Incorrect Password", "The old password is incorrect.")
            return

        # Check if the new password and confirmed password match
        if new_password != confirm_password:
            messagebox.showerror("Password Mismatch", "The new password and confirmed password do not match.")
            return

        # Hash the new password
        hashed_new_password = self.hash_password(new_password)

        username = "Users"
        try:
            db.connect()
            cursor = db.connection.cursor()
            query = "UPDATE users SET password = %s WHERE username = %s"
            cursor.execute(query, (hashed_new_password, username))
            db.connection.commit()
            window.destroy()
        except mysql.connector.Error as error:
            print("Error", str(error))
        finally:
            db.close()

        # Show a success message
        messagebox.showinfo("Password Changed", "Your password has been changed successfully.")
