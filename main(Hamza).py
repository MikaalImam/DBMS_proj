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
            LoginPage.current_emp_id = i_username
            select_query = """SELECT E.Designation
                            FROM Employee E
                            where E.Emp_id = ? and E.Password = ?
                            """
            cursor.execute(select_query, (i_username, i_pass))
            if cursor.fetchval() == True:
                print("OPS")
                #show the ops screen
                self.ops_homepage = Ops_Homepage()
                self.ops_homepage.show()
            else:
                print("HR")
                #show the HR screen
                self.hr_homepage = HR_Homepage()
                self.hr_homepage.show()
        else:
            #pop up saying no such account
            print("error")
        self.close()
        connection.close()

class HR_Homepage(QtWidgets.QMainWindow):
    def __init__(self):
        super(HR_Homepage, self).__init__()
        uic.loadUi("HR homepage.ui", self)
        
        self.pushButton.clicked.connect(self.applicant_management)
        self.pushButton_2.clicked.connect(self.Emp_management)
        self.pushButton_3.clicked.connect(self.close_window)
        
    def applicant_management(self):
        print("applicant")
        self.new_app = new_applicant()
        self.new_app.show()
        
    def Emp_management(self):
        print("Employees")
        self.g_table = guard_table()
        self.g_table.show()
    
    def close_window(self):
        self.close()   
        
class guard_table(QtWidgets.QMainWindow):
    def __init__(self):
        super(guard_table, self).__init__()
        uic.loadUi("Gaurd table.ui", self)
        self.populate_g_table()
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.search_emp)
        self.pushButton_2.clicked.connect(self.update_emp)
        
    def populate_g_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
                        select G.Guard_id, A.F_Name + ' ' + A.L_Name as Name, A.Contact_No, A.Height, A.Weight
                        from Guard G join Application A on G.CNIC = A.CNIC
                        """
        cursor.execute(select_query)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)

        connection.close()
        
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
    def search_emp(self):
        guard_id = self.lineEdit.text()
        name = self.lineEdit_2.text()
    
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
    
        select_query = """ 
                        SELECT G.Guard_id, A.F_Name + ' ' + A.L_Name AS Name, A.Contact_No, A.Height, A.Weight 
                        FROM Guard G JOIN Application A ON G.CNIC = A.CNIC 
                        WHERE G.Guard_id = ? OR A.F_Name LIKE ? OR A.L_Name LIKE ? 
                       """
    
        search_params = [guard_id, f'%{name}%', f'%{name}%']
    
        cursor.execute(select_query, search_params)
    
        
        self.tableWidget.setRowCount(0)
    
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
    
        connection.close()
    
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)        
    
    def update_emp(self):
        print("update")
        selected_row = self.tableWidget.currentRow()
        guard_id  = self.tableWidget.item(selected_row,0).text()
        # name = self.tableWidget.item(selected_row,2).text()
        # contact = self.tableWidget.item(selected_row,3).text()
        # height = self.tableWidget.item(selected_row,4).text()
        # weight = self.tableWidget.item(selected_row,5).text()
        self.up_g = update_g(guard_id)
        self.up_g.show()
        
class update_g(QtWidgets.QMainWindow):
    def __init__(self, guard_id):
        super(update_g, self).__init__()
        uic.loadUi("Update gaurd .ui", self)
        self.guard_id = guard_id
        
        self.pushButton_4.clicked.connect(self.update_it)
        self.pushButton_3.clicked.connect(self.close)
        
        # Populate fields when the window opens
        if self.guard_id:
            self.populate_fields()
    
    def populate_fields(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
        SELECT A.F_Name, A.L_Name, A.CNIC, A.Contact_No, A.Emergency_No, 
               A.Address, A.Weight, A.Height, A.DOB, A.Experience_in_years, 
               A.Status, G.Bank_Account
        FROM Guard G
        JOIN Application A ON G.CNIC = A.CNIC
        WHERE G.Guard_id = ?
        """
        
        cursor.execute(select_query, (self.guard_id,))
        result = cursor.fetchone()
        
        if result:
            self.lineEdit_10.setText(self.guard_id)
            self.lineEdit_10.setReadOnly(True)
            self.lineEdit.setText(result.F_Name)  # First Name
            self.lineEdit_2.setText(result.L_Name)  # Last Name
            self.lineEdit_3.setText(str(result.CNIC))  # CNIC
            self.lineEdit_3.setReadOnly(True)
            self.lineEdit_4.setText(str(result.Contact_No))  # Contact Number
            self.lineEdit_5.setText(str(result.Emergency_No))  # Emergency Number
            self.lineEdit_6.setText(result.Address)  # Address
            self.lineEdit_7.setText(str(result.Weight))  # Weight
            self.lineEdit_8.setText(str(result.Height))  # Height
            
            # Set Date of Birth
            dob = QDate.fromString(str(result.DOB), "yyyy-MM-dd")
            self.dateEdit.setDate(dob)
            
            self.lineEdit_9.setText(str(result.Bank_Account))
        
        connection.close()
    
    def update_it(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
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
        bank_account = self.lineEdit_9.text()
        
        # Update Application table
        update_application_query = """
        UPDATE Application
        SET F_Name = ?, L_Name = ?, DOB = ?, Contact_No = ?, 
            Emergency_No = ?, Address = ?, Weight = ?, Height = ?
        WHERE CNIC = ?
        """
        
        # Update Guard table
        update_guard_query = """
        UPDATE Guard
        SET Bank_Account = ?
        WHERE CNIC = ?
        """
        
        cursor.execute(update_application_query, (f_name, l_name, dob, contact_num, emergency_num, address, weight, height, cnic))
            
        cursor.execute(update_guard_query, (bank_account, cnic))
            
        connection.commit()
        print("Update successful")
        self.close()
        connection.close()
        
        
class new_applicant(QtWidgets.QMainWindow):
    def __init__(self):
        super(new_applicant, self).__init__()
        uic.loadUi("New Applicant.ui", self)
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_4.clicked.connect(self.insert_applicant)
        
    def insert_applicant(self, i_username):
        i_username = LoginPage.current_emp_id
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
        status = 1 if self.radioButton.isChecked() else 0

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Query to insert into the Application table
        insert_application_query = """
                                    INSERT INTO Application (CNIC, F_Name, L_Name, DOB, Contact_No, Emergency_No, Address, Weight, Height, Experience_in_years, Status)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                   """
        cursor.execute(insert_application_query, (cnic, f_name, l_name, dob, contact_num, emergency_num, address, weight, height, experience, status))

        # Query to insert into the Emp_App table
        insert_emp_app_query = """
                                INSERT INTO Emp_App (Emp_id, CNIC)
                                VALUES (?, ?)
                               """
        cursor.execute(insert_emp_app_query, (i_username, cnic))

        # Insert into the Guard table if status is 1
        if status == 1:
            insert_guard_query = """
                                 INSERT INTO Guard (Bank_Account, CNIC)
                                 VALUES (0, ?)
                                 """
            cursor.execute(insert_guard_query, (cnic,))

            connection.commit()




def main():
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()