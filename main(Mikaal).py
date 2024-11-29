# Importing essential modules
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QAbstractItemView
import sys
import pyodbc

server = 'MIKAALIMAM'
database = 'temp_proj'  # Name of your Northwind database
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
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")
            else:
                print("HR")
                #show the HR screen
        else:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("ERROR")
            msgbox.setText("Employee ID or Password was Incorrect")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgbox.setIcon (QtWidgets.QMessageBox.Icon.Warning )   
            msgbox.exec()    
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")

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
        print("shitfs")
        self.shift_table = Shift_Status()
        self.shift_table.show()
            
class Customer_table(QtWidgets.QMainWindow):
    def __init__(self):
        super(Customer_table, self).__init__()
        uic.loadUi("Customer_table.ui", self)

        self.populate_table()
        self.pushButton_2.clicked.connect(self.add_customer)
        self.pushButton_3.clicked.connect(self.edit_cust)




    def populate_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
                        select c.[Cus_name] as [Customer Name], c.[Cus_id] as [Customer_Id], b.[branch_name] as [Branch_Name],
                                b. [branch_id] as [Branch_Id], c.[Contact_num] as [Contact_Number], 
                                (b. [nog_d] + b. [nog_n]) as [Total_Guards]
                        from Customers C join Cust_Branch CB on C.Cus_id = CB.Cus_ID join Branch B on CB.Branc_ID = B.Branch_id
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
        self.close()
        self.add_cust = Add_Customer()
        self.add_cust.show()

    def edit_cust(self):
        selected_row = self.tableWidget.currentRow()
        cus_id  = self.tableWidget.item(selected_row,1).text()
        branc_id = self.tableWidget.item(selected_row,3).text()
        self.close()
        self.edit_cus = Edit_Customer(cus_id, branc_id)
        self.edit_cus.show()

class Add_Customer(QtWidgets.QMainWindow):
    def __init__(self):
        super(Add_Customer, self).__init__()
        uic.loadUi("Add_customer.ui", self)

        self.lineEdit_6.setText(str(i_empid))
        self.lineEdit_6.setDisabled(True)

        self.pushButton_3.clicked.connect(self.close_window)
        self.pushButton_4.clicked.connect(self.insert_customer)        


    def insert_customer(self):
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
                        select count(*)
                        from Customers C
                        where C.Cus_name = ?
                        """
        cursor.execute(select_query,(comp_name))

        if cursor.fetchval() == (1): 
            select_query = """
                        select C.Cus_ID
                        from Customers C
                        where C.Cus_name = ?
                            """
            cursor.execute(select_query,(comp_name))
            cus_id = cursor.fetchval()

            select_query = """
                            insert into Branch (Branch_name, Address , NOG_D, NOG_N, Emp_id)
                            values (?, ?, ?, ?, ?)
                            declare @new_branch int
                            set @new_branch  =  @@identity
                            
                            insert into Cust_Branch (Cus_ID, Branc_ID)
                            values (?, @new_branch)

                            """
            cursor.execute(select_query,(branch_name, addy, gaurds_day, gaurds_night, i_empid, cus_id))
            connection.commit()

        elif cursor.fetchval() == (None):
            select_query = """
                           insert into [Customers] ([Contact_name], [Contact_num], [Cus_name])
                            values (?, ?, ?)
                            declare @new_cus int
                            set @new_cus  =  @@identity

                            insert into Branch (Branch_name, Address , NOG_D, NOG_N, Emp_id)
                            values (?, ?, ?, ?, ?)
                            declare @new_branch int
                            set @new_branch  =  @@identity
                            
                            insert into Cust_Branch (Cus_ID, Branc_ID)
                            values (@new_cus, @new_branch)

                            """
            cursor.execute(select_query,(contact_name, contact_num, comp_name, branch_name, addy, gaurds_day, gaurds_night, i_empid))
            connection.commit()

        connection.close()

        msgbox = QtWidgets.QMessageBox(self)
        msgbox.setWindowTitle("MESSAGE BOX")
        msgbox.setText("New Customer Added Succesfully")
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msgbox.setIcon (QtWidgets.QMessageBox.Icon.Information)   
        msgbox.exec()    


        self.close()


    def close_window(self):
        self.close()

class Edit_Customer(QtWidgets.QMainWindow):
    def __init__(self, c_id, b_id):
        super(Edit_Customer, self).__init__()
        uic.loadUi("update_customer.ui", self)

        self.c_id = c_id
        self.b_id = b_id
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
                    select c.[Cus_name] as [Customer Name], b.[branch_name] as [Branch_Name], B.Address as addy,
                            c.[Contact_num] as [Contact_Number], C.Contact_name ,
                            b. [nog_d] as gaurds_day , b. [nog_n] as gaurds_night
                    from Customers C join Cust_Branch CB on C.Cus_id = CB.Cus_ID join Branch B on CB.Branc_ID = B.Branch_id
                    where C.Cus_id = ? and B.branch_id = ?
                    """
        cursor.execute(select_query, (c_id, b_id))
        
        temp_tuple = cursor.fetchall()[0]


        self.lineEdit_6.setText(str(i_empid))
        self.lineEdit_6.setDisabled(True)

        self.lineEdit.setText(str(temp_tuple[0]))
        self.lineEdit_2.setText(str(temp_tuple[1]))
        self.lineEdit_3.setText(str(temp_tuple[2]))
        self.lineEdit_4.setText(str(temp_tuple[4]))
        self.lineEdit_5.setText(str(temp_tuple[3]))
        self.lineEdit_7.setText(str(temp_tuple[5]))
        self.lineEdit_8.setText(str(temp_tuple[6]))


        self.pushButton_3.clicked.connect(self.close_window)
        self.pushButton_4.clicked.connect(self.insert_edited_cus)

        connection.close()
        
    def insert_edited_cus(self):
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
                update [Customers]
                set [Contact_name] = ?,
                    [Contact_num] = ?,
                    [Cus_name] = ?
                where [Cus_id] = ?

                update Branch 
                set Branch_name = ?,
                    Address = ?, 
                    NOG_D = ?, 
                    NOG_N = ?
                where branch_id = ?
                declare @new_branch int
                set @new_branch  =  @@identity
                """
        cursor.execute(select_query,(contact_name, contact_num, comp_name, self.c_id, branch_name, addy, gaurds_day, gaurds_night, self.b_id))
        connection.commit()

        msgbox = QtWidgets.QMessageBox(self)
        msgbox.setWindowTitle("MESSAGE BOX")
        msgbox.setText("Customer Edited Succesfully")
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msgbox.setIcon (QtWidgets.QMessageBox.Icon.Information)   
        msgbox.exec()    

        connection.close()

        self.close()

    def close_window(self):
        self.close()

class Shift_Status(QtWidgets.QMainWindow):
    def __init__(self):
        super(Shift_Status, self).__init__()
        uic.loadUi("shift_table.ui", self)

        self.tableWidget.setSortingEnabled(True)

        self.populate_table()

        self.pushButton_4.clicked.connect(self.view_shift)
        self.pushButton_3.clicked.connect(self.assign_guards)

    def populate_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
                        select S.shift_id ,datename(weekday, s.Date) as day, C.Cus_name, C.Cus_id, B.Branch_name, B.Branch_id, 
                            case 
                            when S.Shift_D_N = 0 then 'Day'
                            else 'Night'
                            end as shit_type, 

                            case 
                            when S.Shift_D_N = 0 and (select count(Guard_id) from Shift_Guard SG where SG.Shift_id = S.Shift_id) < B.NOG_D then 'INCOMPLETE'
                            when S.Shift_D_N = 1 and (select count(Guard_id) from Shift_Guard SG where SG.Shift_id = S.Shift_id) < B.NOG_N then 'INCOMPLETE'
                            else 'COMPLETE'
                            end as status, 

                            case
                            when S.Shift_D_N = 0 then B.NOG_D - (select count(Guard_id) from Shift_Guard SG where SG.Shift_id = S.Shift_id)  
                            when S.Shift_D_N = 1 then B.NOG_N - (select count(Guard_id) from Shift_Guard SG where SG.Shift_id = S.Shift_id)
                            else 0
                            end as gaurds_needed 
                    from Shifts S join Branch B on S.branch_id = B.Branch_id
                        join Cust_Branch CB on B.Branch_id = CB.Branc_ID
                        join Customers C on CB.Cus_ID = C.Cus_id
                        """
        cursor.execute(select_query)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)

        self.tableWidget.sortByColumn(1, QtCore.Qt.SortOrder.AscendingOrder)
        
        connection.close()
        
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)

    def view_shift(self):
        selected_row = self.tableWidget.currentRow()
        Shift_id  = self.tableWidget.item(selected_row,0).text()
        comp_name  = self.tableWidget.item(selected_row,2).text()
        branch_name = self.tableWidget.item(selected_row,4).text()
        c_id = self.tableWidget.item(selected_row,3).text()
        b_id = self.tableWidget.item(selected_row,5).text()
        self.view_shift_detail = View_shift(comp_name, branch_name, b_id, Shift_id) 
        self.view_shift_detail.show()

    def assign_guards(self):
        selected_row = self.tableWidget.currentRow()
        Shift_id  = self.tableWidget.item(selected_row,0).text()
        comp_name  = self.tableWidget.item(selected_row,2).text()
        branch_name = self.tableWidget.item(selected_row,4).text()
        b_id = self.tableWidget.item(selected_row,5).text()
        self.assign_new_gaurds = Assign_gaurds(comp_name, branch_name, b_id, Shift_id)
        self.assign_new_gaurds.show()
        self.close()

class View_shift(QtWidgets.QMainWindow):
    def __init__(self, comp_name, branch_name, b_id, s_id):
        super(View_shift, self).__init__()
        uic.loadUi("View_guards.ui", self)


        self.pushButton_4.clicked.connect(self.close_window)

        
        self.shift_id = s_id

        self.lineEdit_10.setText(str(comp_name))
        self.lineEdit_10.setDisabled(True)

        self.lineEdit_9.setText(str(branch_name))
        self.lineEdit_9.setDisabled(True)

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
                        select NOG_D, NOG_N
                        from Branch B
                        where B.Branch_id = ?
                        """
        cursor.execute(select_query, (b_id))

        temp_NOG = cursor.fetchall()[0]

        select_query = """
                        Select S.Shift_D_N
                        from Shifts S
                        where S.Shift_id = ?
                        """
        cursor.execute(select_query, (s_id))

        temp = cursor.fetchall()[0]
        if (temp[0] == True):
            self.lineEdit_7.setText(str("Night"))
            self.lineEdit_7.setDisabled(True)
            self.lineEdit_8.setText(str(temp_NOG[1]))
            self.lineEdit_8.setDisabled(True)
            
        else:
            self.lineEdit_7.setText(str("Day"))
            self.lineEdit_7.setDisabled(True)
            self.lineEdit_8.setText(str(temp_NOG[0]))
            self.lineEdit_8.setDisabled(True)
            



        connection.close()


        self.populate_table()
        

    def populate_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
                        select
                        g. [Guard_id] as Guard_ID,
                        a. [F_Name] ++ a. [L_Name] as Name,
                        DateDiff(Year, a.DOB, getdate()) as Age,
                        a. [Height] as Height,
                        a. [Weight] as weight
                        from
                        Shifts s inner join [Shift_Guard] sg on s. [Shift_id] = sg. [Shift_id]
                        inner join [Guard] g on sg. [Guard_id] = g. [Guard_id]
                        inner join [Application] a on a.CNIC = g.CNIC
                        where
                        s. [Shift_id] = ? 
                        """
        cursor.execute(select_query, (self.shift_id))

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

    def close_window(self):
        self.close()

class Assign_gaurds(QtWidgets.QMainWindow):
    def __init__(self, comp_name, branch_name, b_id, Shift_id):
        super(Assign_gaurds, self).__init__()
        uic.loadUi("Assign_gaurds.ui", self)

        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)




        self.pushButton_5.clicked.connect(self.assign_gaurds)
        self.pushButton_6.clicked.connect(self.close_window)



        self.shift_id = Shift_id

        self.lineEdit_10.setText(str(comp_name))
        self.lineEdit_10.setDisabled(True)

        self.lineEdit_9.setText(str(branch_name))
        self.lineEdit_9.setDisabled(True)

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
                        select NOG_D, NOG_N
                        from Branch B
                        where B.Branch_id = ?
                        """
        cursor.execute(select_query, (b_id))

        self.temp_NOG = cursor.fetchall()[0]

        select_query = """
                        Select S.Shift_D_N , S.Date
                        from Shifts S
                        where S.Shift_id = ?
                        """
        cursor.execute(select_query, (Shift_id))

        temp = cursor.fetchall()[0]
        self.shift_d_n = temp[0]
        self.date = temp[1]

        select_query = """
                        (select count(Guard_id) 
                        from Shift_Guard SG 
                        where SG.Shift_id = ?)
                        """
        cursor.execute(select_query, (Shift_id))
        self.num_g_current = cursor.fetchall()[0]

        if (temp[0] == True):
            self.lineEdit_12.setText(str("Night"))
            self.lineEdit_12.setDisabled(True)
            self.lineEdit_7.setText(str(self.temp_NOG[1]-self.num_g_current[0]))
            self.lineEdit_7.setDisabled(True)
            
        else:
            self.lineEdit_12.setText(str("Day"))
            self.lineEdit_12.setDisabled(True)
            self.lineEdit_7.setText(str(self.temp_NOG[0]-self.num_g_current[0]))
            self.lineEdit_7.setDisabled(True)
            
        self.lineEdit_11.setText(str(temp[1]))
        self.lineEdit_11.setDisabled(True)

        connection.close()

        self.populate_table()

    def populate_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        select_query = """
                    select G.Guard_id, A.F_Name + ' ' + A.L_Name as Name, DATEDIFF(YEAR, A.DOB, GETDATE()), Height, Weight
                    from Guard G join Application A on G.CNIC = A.CNIC
                    where G.Guard_id not in 
                    (select SG.Guard_id from Shifts S join Shift_Guard SG on S.Shift_id = SG.Shift_id where S.Date = ? and S.Shift_D_N = ?)
                        """
        cursor.execute(select_query, (self.date, self.shift_d_n))

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

    def assign_gaurds(self):
        # Get the selected rows
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        # List to store selected row IDs (indices)
        selected_row_ids = []

        # Loop through selected rows and get the row index for each
        for index in selected_rows:
            selected_row_ids.append(index.row())  # Get the row index

        # Print the selected row indices
        print("Selected row indices:", selected_row_ids)
        print(len(selected_row_ids))

        if (self.shift_d_n == True):
            i = 1
        else: 
            i = 0        

        if (len(selected_row_ids) > (self.temp_NOG[i]-self.num_g_current[0])):
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("ERROR")
            msgbox.setText("Assigning More gaurds than required to a shift")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgbox.setIcon (QtWidgets.QMessageBox.Icon.Warning)   
            msgbox.exec()    
        else:
            for index in selected_row_ids:
                gaurd_id = (self.tableWidget.item(selected_row_ids[index],0).text())

                connection = pyodbc.connect(connection_string)
                cursor = connection.cursor()
                select_query = """
                                insert into Shift_Guard (Shift_id, Guard_id) values (?, ?)
                                """
                cursor.execute(select_query, (self.shift_id, gaurd_id))
                connection.commit()



                msgbox = QtWidgets.QMessageBox(self)
                msgbox.setWindowTitle("MESSAGE BOX")
                msgbox.setText("Gaurds Assigned to shifts Succesfully")
                msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msgbox.setIcon (QtWidgets.QMessageBox.Icon.Information)   
                msgbox.exec()    

                connection.close()

                self.close()


    def close_window(self):
        self.close()    


def main():
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
