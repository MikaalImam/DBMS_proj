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
        
        # select_query = "SELECT * FROM Employee"
        # cursor.execute(select_query)
        # print("All Employee:")
        # for row in cursor.fetchall():
        #     print(row)

        # connection.close()

    def check_login(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        select_query = "SELECT * FROM Employee"
        cursor.execute(select_query)
        print("All Employee:")

        for row in cursor.fetchall():
            print(row)

        # Use parameterized queries to safely handle user input
        global i_empid
        i_empid = int(self.lineEdit.text())
        i_pass = self.lineEdit_2.text()

        # Parameterized query to prevent SQL injection
        select_query = """SELECT COUNT(*)
                            FROM Employee E
                            WHERE E.Emp_id = ? AND E.Password = ?"""
        cursor.execute(select_query, (i_empid, i_pass))


        if cursor.fetchval() == (1):
            select_query = """SELECT E.Designation
                            FROM Employee E
                            where E.Emp_id = ? and E.Password = ?
                            """
            cursor.execute(select_query, (i_empid, i_pass))
            if cursor.fetchval() == True:
                print("OPS")
                #show the ops screen
                self.ops_homepage = Ops_Homepage()
                self.ops_homepage.show()
            else:
                print("HR")
                #show the HR screen
        else:
            #pop up saying no such account
            print("error")

        connection.close()

class Ops_Homepage(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ops_Homepage, self).__init__()
        uic.loadUi("ops_homepage.ui", self)
        
        self.pushButton.clicked.connect(self.Customer_managment)
        self.pushButton_2.clicked.connect(self.Emp_schdule_managment)
        

    def Customer_managment(self):
        print("cusomter")
        self.cust_table = Customer_table()
        self.cust_table.show()
    
    def Emp_schdule_managment(self):
        print("emp scdule")
            
class Customer_table(QtWidgets.QMainWindow):
    def __init__(self):
        super(Customer_table, self).__init__()
        uic.loadUi("Customer_table.ui", self)

        self.pushButton_2.clicked.connect(self.add_customer)
        self.populate_table()


    def populate_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
                        select c.[Cus_name] as [Customer Name], c.[Cus_id] as [Customer_Id], b.[branch_name] as [Branch_Name],
                             b. [branch_id] as [Branch_Id], c.[Contact_num] as [Contact_Number], 
                             (b. [nog_d] + b. [nog_n]) as [Total_Guards]
                        from [Customers] c left join [Branch] b on c. [Cus_id] = b. [branch_id]
                        order by c. [Cus_name], b. [branch_id]
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
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)

    def add_customer(self):
        self.add_cust = Add_Customer()
        self.add_cust.show()

class Add_Customer(QtWidgets.QMainWindow):
    def __init__(self):
        super(Add_Customer, self).__init__()
        uic.loadUi("Add_customer.ui", self)

        self.lineEdit_6.setText(str(i_empid))
        self.lineEdit_6.setDisabled(True)

        self.pushButton_3.clicked.connect(self.insert_customer)
        self.pushButton_4.clicked.connect(self.insert_customer)
        


    def insert_customer(self):
        emp_resp = i_empid
        comp_name = self.lineEdit.text()
        branch_name = self.lineEdit_2.text()
        addy = self.lineEdit_3.text()
        contact_name = self.lineEdit_4.text()
        contact_num = self.lineEdit_5.text()
        gaurds_day = self.lineEdit_7.text()
        gaurds_night = self.lineEdit_8.text()

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """

                        """
        cursor.execute(select_query)


    def close_window(self):
        print("ufuf")

# create procedure AddCustomerWithBranch
# @ContactName varchar,
# @ContactNum int,
# @CusName varchar,
# @BranchName varchar,
# @NogD int,
# @NogN int
# as
# begin
# declare @CustomerId int
# declare @BranchId int
# insert into [Customers] ([Contact_name], [Contact_num], [Cus_name])
# values (@ContactName, @ContactNum, @CusName select @CustomerId = [Cus_id] from [Customers])
# where [Contact_name] @ContactName and [Contact_num] @ContactNum


# insert into [Branch] ([branch_name], [nog_d], [nog_n])
# values (@BranchName, @NogD, @NogN)
# select @BranchId [branch_id] from [Branch]
# where [branch_name] = @BranchName and [nog_d] @NogD and [nog_n] = @NogN
# insert into [Cust_Branch] ([Cus_id], [Branc_ID])
# values (@CustomerId, @BranchId)
# print 'Customer and Branch added successfully'
# end
# --Example
# exec AddCustomerWithBranch @ContactName John Doe, @ContactNum = 1234567890, @CusName Tech Innovators", @BranchName Karachi Branch @NogD 3,@NogN=2;




def main():
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


