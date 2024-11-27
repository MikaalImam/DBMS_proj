# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

server = 'DESKTOP-N7IP310\\SQLSERVER'
database = 'Project'  # Name of your Northwind database
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
                # self.ops_homepage = Ops_Homepage()
                self.ops_homepage.show()
            else:
                print("HR")
                #show the HR screen
                self.hr_homepage = HR_Homepage()
                self.hr_homepage.show()
        else:
            #pop up saying no such account
            print("error")

        connection.close()

class HR_Homepage(QtWidgets.QMainWindow):
    def __init__(self):
        super(HR_Homepage, self).__init__()
        uic.loadUi("HR homepage.ui", self)
        
        self.pushButton.clicked.connect(self.applicant_management)
        self.pushButton_2.clicked.connect(self.Emp_management)
        
    def applicant_management(self):
        print("applicant")
        self.new_app = new_applicant()
        self.new_app.show()
        
    def Emp_management(self):
        print("Employees")
        
class new_applicant(QtWidgets.QMainWindow):
    def __init__(self):
        super(new_applicant, self).__init__()
        uic.loadUi("New Applicant.ui", self)
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_4.clicked.connect(self.insert_applicant)
        
    def insert_applicant(self):
        f_name = self.lineEdit.text()
        l_name = self.lineEdit_2.text()
        cnic = self.lineEdit_3.text()
        contact_num = self.lineEdit_4.text()
        emergency_num = self.lineEdit_5.text()
        address = self.lineEdit_6.text()
        weight = float(self.lineEdit_7.text())
        height = float(self.lineEdit_8.text())
        dob_qdate = self.dateEdit.date()
        dob = dob_qdate.toString("yyyy-MM-dd")
        experience = self.comboBox.currentText()
        status = "Accepted" if self.radioButton.isChecked() else "Rejected"
    
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        insert_query = """
                    INSERT INTO Application (CNIC, F_Name, L_Name, DOB, Contact_No, Emergency_No, Address, Weight, Height, Experience_in_years, Status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   """
    
        cursor.execute(insert_query, (cnic, f_name, l_name, dob, contact_num, emergency_num, address, weight, height, experience, status))
        connection.commit()


def main():
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()