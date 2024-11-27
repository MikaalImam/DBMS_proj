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
(1122334455667, N'Muhammad', N'Usman', cast('1988-03-03' as date), 564738291, 192837465, N'789 Oak Avenue', 80.0, 175.0, 7, 1);  -- Active applicant

-- Insert data into [Guard] table
INSERT INTO [Guard] ([Bank_Account], [CNIC])
VALUES 
(N'PKR-123456789', 1234567890123),  -- Guard 1 with CNIC 1234567890123
(N'PKR-987654321', 9876543210987),  -- Guard 2 with CNIC 9876543210987
(N'PKR-112233445', 1122334455667);  -- Guard 3 with CNIC 1122334455667

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

-- Insert data into [Emp_App] table
INSERT INTO [Emp_App] ([Emp_id], [CNIC])
VALUES 
(1, 1234567890123),  -- Emp_id 1 corresponds to Ahmed Ali with CNIC 1234567890123
(1, 9876543210987),  -- Emp_id 1 corresponds to Fatima Khan with CNIC 9876543210987
(3, 1122334455667);  -- Emp_id 3 corresponds to Muhammad Usman with CNIC 1122334455667

-- Insert data into [Shifts] table
INSERT INTO [Shifts] ([Date], [Shift_D_N], [Emp_id], [branch_id])
VALUES
(cast('2024-11-16' as date), 1, 2, 1), 
(cast('2024-11-16' as date), 0, 2, 1), 
(cast('2024-11-17' as date), 0, 2, 2),
(cast('2024-11-17' as date), 1, 2, 4), 
(cast('2024-11-18' as date), 1, 2, 3);  


-- Insert data into [Shift-Guard] table
INSERT INTO [Shift_Guard] ([Shift_id], [Guard_id])
VALUES
(1, 1),  -- Shift 1 assigned to Guard 1
(2, 2),  -- Shift 2 assigned to Guard 2
(3, 3),
(4, 1),
(5, 2);  -- Shift 3 assigned to Guard 3








