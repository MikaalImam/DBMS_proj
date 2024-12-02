CREATE TABLE [Customers] (
	[Cus_id] int IDENTITY(1,1) NOT NULL UNIQUE,
	[Contact_name] nvarchar(max)  NOT NULL,
	[Contact_num] bigint NOT NULL,
	[Cus_name] nvarchar(max)  NOT NULL,
	PRIMARY KEY ([Cus_id])
);

CREATE TABLE [Employee] (
	[Emp_id] int IDENTITY(1,1) NOT NULL UNIQUE,
	[Password] nvarchar(max) NOT NULL,
	[Name] nvarchar(max) NOT NULL,
	[Designation] bit NOT NULL,
	PRIMARY KEY ([Emp_id])
);

CREATE TABLE [Emp_App] (
	[Emp_id] int NOT NULL,
	[CNIC] bigint NOT NULL,
	PRIMARY KEY ([Emp_id], [CNIC])
);

CREATE TABLE [Shifts] (
	[Shift_id] int IDENTITY(1,1) NOT NULL UNIQUE,
	[Date] date NOT NULL,
	[Shift_D_N] bit NOT NULL,
	[Emp_id] int NOT NULL,
	[branch_id] int NOT NULL,
	PRIMARY KEY ([Shift_id])
);

CREATE TABLE [Shift_Guard] (
	[Shift_id] int NOT NULL,
	[Guard_id] int NOT NULL,
	PRIMARY KEY ([Shift_id], [Guard_id])
);

CREATE TABLE [Application] (
	[CNIC] bigint NOT NULL UNIQUE,
	[F_Name] nvarchar(max) NOT NULL,
	[L_Name] nvarchar(max) NOT NULL,
	[DOB] date NOT NULL,
	[Contact_No] bigint NOT NULL,
	[Emergency_No] bigint NOT NULL,
	[Address] nvarchar(max) NOT NULL,
	[Weight] float(53) NOT NULL,
	[Height] float(53) NOT NULL,
	[Experience_in_years] int NOT NULL,
	[Status] bit NOT NULL,
	PRIMARY KEY ([CNIC])
);

CREATE TABLE [Guard] (
	[Guard_id] int IDENTITY(1,1) NOT NULL UNIQUE,
	[Bank_Account] nvarchar(max) NOT NULL,
	[CNIC] bigint NOT NULL,
	PRIMARY KEY ([Guard_id])
);

CREATE TABLE [Branch] (
	[Branch_id] int IDENTITY(1,1) NOT NULL UNIQUE,
	[Branch_name] nvarchar(max) NOT NULL,
	[Address] nvarchar(max) NOT NULL,
	[NOG_D] int NOT NULL,
	[NOG_N] int NOT NULL,
	[Emp_id] int NOT NULL,
	PRIMARY KEY ([Branch_id])
);

CREATE TABLE [Cust_Branch] (
	[Cus_ID] int NOT NULL,
	[Branc_ID] int NOT NULL,
	PRIMARY KEY ([Cus_ID], [Branc_ID])
);



ALTER TABLE [Emp_App] ADD CONSTRAINT [Emp_App_fk0] FOREIGN KEY ([Emp_id]) REFERENCES [Employee]([Emp_id]);

ALTER TABLE [Emp_App] ADD CONSTRAINT [Emp_App_fk1] FOREIGN KEY ([CNIC]) REFERENCES [Application]([CNIC]);
ALTER TABLE [Shifts] ADD CONSTRAINT [Shifts_fk3] FOREIGN KEY ([Emp_id]) REFERENCES [Employee]([Emp_id]);

ALTER TABLE [Shifts] ADD CONSTRAINT [Shifts_fk4] FOREIGN KEY ([branch_id]) REFERENCES [Branch]([Branch_id]);
ALTER TABLE [Shift_Guard] ADD CONSTRAINT [Shift_Guard_fk0] FOREIGN KEY ([Shift_id]) REFERENCES [Shifts]([Shift_id]);

ALTER TABLE [Shift_Guard] ADD CONSTRAINT [Shift_Guard_fk1] FOREIGN KEY ([Guard_id]) REFERENCES [Guard]([Guard_id]);

ALTER TABLE [Guard] ADD CONSTRAINT [Guard_fk2] FOREIGN KEY ([CNIC]) REFERENCES [Application]([CNIC]);
ALTER TABLE [Branch] ADD CONSTRAINT [Branch_fk4] FOREIGN KEY ([Emp_id]) REFERENCES [Employee]([Emp_id]);
ALTER TABLE [Cust_Branch] ADD CONSTRAINT [Cust_Branch_fk0] FOREIGN KEY ([Cus_ID]) REFERENCES [Customers]([Cus_id]);

ALTER TABLE [Cust_Branch] ADD CONSTRAINT [Cust_Branch_fk1] FOREIGN KEY ([Branc_ID]) REFERENCES [Branch]([Branch_id]);

-- Insert data into [Customers] table
INSERT INTO [Customers] ([Contact_name], [Contact_num], [Cus_name])
VALUES 
('John Doe', 1234567890, 'Shell'),
('Jane Smith', 9876543210, 'Imtiaz'),
('Robert Brown', 5647382910, 'Habib');

-- Insert data into [Employee] table
INSERT INTO [Employee] ([Password], [Name], [Designation])
VALUES 
(N'password123', N'Ahmed Ali', 1),  
(N'password456', N'Fatima Khan', 0),
(N'password789', N'Muhammad Usman', 1);



-- Insert data into [Application] table
INSERT INTO [Application] ([CNIC], [F_Name], [L_Name], [DOB], [Contact_No], [Emergency_No], [Address], [Weight], [Height], [Experience_in_years], [Status])
VALUES 
(1234567890123, N'Ahmed', N'Ali', cast('1990-01-01' as date), 123456789, 987654321, N'123 Main Street', 70.5, 180.0, 5, 1),  -- Active applicant
(9876543210987, N'Fatima', N'Khan', cast('1992-02-02' as date), 987654321, 123123123, N'456 Elm Street', 55.0, 165.0, 3, 1),  -- Inactive applicant
(1111111111111, N'mikaal', N'Imam', cast('1995-10-24' as date), 123456789, 123748596, N'123 elm street', 22.0, 125.0, 5, 0),
(1122334455667, N'Muhammad', N'Usman', cast('1988-03-03' as date), 564738291, 192837465, N'789 Oak Avenue', 80.0, 175.0, 7, 1),  -- Active applicant
(3344556677889, N'Sarah', N'Malik', cast('1985-06-15' as date), 345678901, 234567890, N'321 Pine Road', 65.0, 160.0, 10, 1),  -- Active applicant
(6677889900112, N'Zain', N'Raza', cast('1990-12-10' as date), 567890123, 765432109, N'654 Birch Blvd', 72.0, 178.0, 4, 0),  -- Inactive applicant
(9988776655443, N'Fariha', N'Zahid', cast('1987-09-23' as date), 765432109, 345678901, N'987 Cedar Lane', 58.0, 170.0, 8, 1),  -- Active applicant
(1122334455990, N'Ali', N'Rashid', cast('1995-07-30' as date), 876543210, 123789456, N'159 Maple Street', 78.0, 185.0, 6, 0),  -- Inactive applicant
(2233445566778, N'Imran', N'Sheikh', cast('1993-01-20' as date), 234567890, 345678901, N'456 Willow Rd', 90.0, 190.0, 9, 1),  -- Active applicant
(3344556677880, N'Ayesha', N'Mushtaq', cast('1994-11-05' as date), 456789012, 234567891, N'789 Chestnut Ave', 54.5, 162.0, 2, 0),  -- Inactive applicant
(5566778899001, N'Jameela', N'Bashir', cast('1980-04-12' as date), 987654320, 123456780, N'432 Pine Street', 68.0, 167.0, 15, 1),  -- Active applicant
(7766554433220, N'Farhan', N'Khan', cast('1991-02-25' as date), 234567891, 987654312, N'654 Ash Blvd', 82.0, 179.0, 7, 0);  -- Inactive applicant


-- Insert data into [Guard] table
INSERT INTO [Guard] ([Bank_Account], [CNIC])
VALUES
(N'PKR-123456789', 1234567890123),  -- Bank account PKR-123456789 linked to CNIC 1234567890123 (Ahmed Ali)
(N'PKR-987654321', 9876543210987),  -- Bank account PKR-987654321 linked to CNIC 9876543210987 (Fatima Khan)
(N'PKR-112233456', 1111111111111),  -- Bank account PKR-112233456 linked to CNIC 1111111111111 (Mikaal Imam)
(N'PKR-223344567', 1122334455667),  -- Bank account PKR-223344567 linked to CNIC 1122334455667 (Muhammad Usman)
(N'PKR-334455678', 3344556677889),  -- Bank account PKR-334455678 linked to CNIC 3344556677889 (Sarah Malik)
(N'PKR-445566789', 6677889900112),  -- Bank account PKR-445566789 linked to CNIC 6677889900112 (Zain Raza)
(N'PKR-556677890', 9988776655443),  -- Bank account PKR-556677890 linked to CNIC 9988776655443 (Fariha Zahid)
(N'PKR-667788901', 1122334455990),  -- Bank account PKR-667788901 linked to CNIC 1122334455990 (Ali Rashid)
(N'PKR-778899012', 2233445566778),  -- Bank account PKR-778899012 linked to CNIC 2233445566778 (Imran Sheikh)
(N'PKR-889900123', 3344556677880),  -- Bank account PKR-889900123 linked to CNIC 3344556677880 (Ayesha Mushtaq)
(N'PKR-990011234', 5566778899001),  -- Bank account PKR-990011234 linked to CNIC 5566778899001 (Jameela Bashir)
(N'PKR-101112345', 7766554433220);  -- Bank account PKR-101112345 linked to CNIC 7766554433220 (Farhan Khan)



-- Insert data into [Branch] table
INSERT INTO [Branch] ([Branch_name], [Address] , [NOG_D], [NOG_N], [Emp_id])
VALUES 
(N'Karachi Branch', 'yes street' , 5, 3, 2), 
(N'Lahore Branch', 'mhmm street' ,4, 4, 2),  
(N'Peshawar Branch', 'lol street',2, 2, 2),  
(N'Islamabad Branch', 'boo street',6, 2, 2);  

-- Insert data into [Cust_Branch] table
INSERT INTO [Cust_Branch] ([Cus_ID], [Branc_ID])
VALUES
(1, 1),  -- Customer 1 is associated with Karachi Branch
(1, 2),  -- Customer 2 is associated with Lahore Branch
(2, 3),  -- Customer 3 is associated with Islamabad Branch
(3, 4);


-- Mapping CNIC numbers to Employee IDs (1 or 3)
INSERT INTO [Emp_App] ([Emp_ID], [CNIC])
VALUES
(1, 1234567890123),  -- Emp_id 1 corresponds to Ahmed Ali with CNIC 1234567890123
(1, 9876543210987),  -- Emp_id 1 corresponds to Fatima Khan with CNIC 9876543210987
(3, 1111111111111),  -- Emp_id 3 corresponds to Mikaal Imam with CNIC 1111111111111
(3, 1122334455667),  -- Emp_id 3 corresponds to Muhammad Usman with CNIC 1122334455667
(1, 3344556677889),  -- Emp_id 1 corresponds to Sarah Malik with CNIC 3344556677889
(3, 6677889900112),  -- Emp_id 3 corresponds to Zain Raza with CNIC 6677889900112
(1, 9988776655443),  -- Emp_id 1 corresponds to Fariha Zahid with CNIC 9988776655443
(3, 1122334455990),  -- Emp_id 3 corresponds to Ali Rashid with CNIC 1122334455990
(1, 2233445566778),  -- Emp_id 1 corresponds to Imran Sheikh with CNIC 2233445566778
(3, 3344556677880),  -- Emp_id 3 corresponds to Ayesha Mushtaq with CNIC 3344556677880
(1, 5566778899001),  -- Emp_id 1 corresponds to Jameela Bashir with CNIC 5566778899001
(3, 7766554433220);  -- Emp_id 3 corresponds to Farhan Khan with CNIC 7766554433220



-- Insert data into [Shifts] table
INSERT INTO [Shifts] ([Date], [Shift_D_N], [Emp_id], [branch_id])
VALUES
(cast('2024-11-16' as date), 1, 2, 1), 
(cast('2024-11-16' as date), 0, 2, 1), 
(cast('2024-11-17' as date), 0, 2, 2),
(cast('2024-11-17' as date), 1, 2, 4), 
(cast('2024-11-18' as date), 1, 2, 3),   
(cast('2024-11-19' as date), 1, 2, 2), 
(cast('2024-11-19' as date), 1, 2, 4); 



-- Insert data into [Shift-Guard] table
INSERT INTO [Shift_Guard] ([Shift_id], [Guard_id])
VALUES
(1, 1),  -- Shift 1 assigned to Guard 1
(2, 2),  -- Shift 2 assigned to Guard 2
(3, 3),
(4, 1),
(5, 2);  -- Shift 3 assigned to Guard 3








