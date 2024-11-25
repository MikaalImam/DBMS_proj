# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

server = 'MIKAALIMAM'
database = 'Proj_db'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'your_username'  # Specify a username if not using Windows Authentication
password = 'your_password'  # Specify a password if not using Windows Authentication

if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'




class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginPage, self).__init__()
        uic.loadUi("Login_Page.ui", self)
        self.pushButton.clicked.connect(self.check_login)


        connection = pyodbc.connect(connection_string)
        # Create a cursor to interact with the database
        cursor = connection.cursor()
        
        select_query = "SELECT * FROM Employee"
        cursor.execute(select_query)
        print("All Employee:")
        for row in cursor.fetchall():
            print(row)

        connection.close()

    def check_login(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        select_query = "SELECT * FROM Employee"
        cursor.execute(select_query)
        print("All Employee:")

        for row in cursor.fetchall():
            print(row)

        # Use parameterized queries to safely handle user input
        i_username = int(self.lineEdit.text())
        i_pass = self.lineEdit_2.text()

        # Parameterized query to prevent SQL injection
        select_query = """SELECT COUNT(*)
                            FROM Employee E
                            WHERE E.Emp_id = ? AND E.Password = ?"""
        cursor.execute(select_query, (i_username, i_pass))


        if cursor.fetchval() == (1):
            select_query = """SELECT E.Designation
                            FROM Employee E
                            where E.Emp_id = ? and E.Password = ?
                            """
            cursor.execute(select_query, (i_username, i_pass))
            if cursor.fetchval() == True:
                print("OPS")
                #show the ops screen
            else:
                print("HR")
                #show the HR screen
        else:
            #pop up saying no such account
            print("error")

        connection.close()



def main():
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


