#imports
from hashlib import sha256
import sqlite3

#creates a new database if one doesn't exist already and allocates a cursor to navigate it
conn = sqlite3.connect('testdb.db')
cursor = conn.cursor()

def createOriginalUsernamePassword():
    username = input("please enter an original username: ")
    password = input("please enter an original password: ")
    return username, password

class Conversion():
    def Convert(input):
        return sha256(input.encode('utf-8')).hexdigest()

class sqliteModification():
    def CheckTable():
        #query to check if username table exists in sqlite3 database
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users'")
        username_table_exists = cursor.fetchone()[0]
        if username_table_exists == 0:
            #creates new table if one doesn't exist
            print("Creating new table")
            cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
            Conversion.createOriginalUsernamePassword()
        else:
            if (sqliteModification.checkTableEmptiness() == True):
                print('Table is empty')
    def checkTableEmptiness():
        cursor.execute("SELECT count(*) FROM users")
        table_empty = cursor.fetchone()[0]
        if table_empty == 0:
            username, password = createOriginalUsernamePassword()
            print(username, password)
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, Conversion.Convert(password)))
            conn.commit()
        else:
            sqliteModification.checkPassword()
    
    def checkPassword():
        print("Username/password combo already exists. Enter Y to login or N to create a new account")
        answer = input()
        if answer == "Y":
            username = input("Username: ")
            password = Conversion.Convert(input("Password: "))
            if username == cursor.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone()[0]:
                if password == cursor.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()[0]:
                    print("Login successful")
                else:
                    print("Password incorrect")
        else:
            sqliteModification.enterNewLogin()
    def enterNewLogin():
        username = input("Username: ")
        password = Conversion.Convert(input("Password: "))
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

              

sqliteModification.CheckTable()


    
