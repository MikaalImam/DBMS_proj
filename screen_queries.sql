--screen 1 (Login)
--there will be some sort of an if condition that will 
--check if the count of the entered user name and pass is one 
--ie is uniqeue and then depending on the designation it will check display the relevent screens
select count(*)
from Employee E
where E.Emp_id = i_username and E.Password = i_pass

--to display the write screens to the right employee
select E.Designation
from Employee E
where E.Emp_id = i_username 


--screen 3 (New applicant screen)
create procedure Add_applicant
	@Cnic bigint, 
	@F_name varchar, 
	@L_name varchar, 
	@DOB date, 
	@Contact_num bigint, 
	@Emergency_num bigint, 
	@address varchar, 
	@weight float, 
	@height float, 
	@experience int, 
	@status bit,
	@empid int
as 
begin

insert into Application(CNIC, F_Name, L_Name, DOB, Contact_No, Emergency_No, Address, Weight, Height, Experience_in_years, Status ) 
values (@Cnic, @F_name, @L_name, @DOB, @Contact_num, @Emergency_num, @address, @weight, @height, @experience, @status)

insert into Emp_App(Emp_id, CNIC) values (@empid, @Cnic)
end

--screen 4 (Gaurd Table)
create procedure displaygaurds
	@guard_id int,
	@name varchar
as 
begin
select G.Guard_id, A.F_Name + ' ' + A.L_Name as Name, A.Contact_No, A.Height, A.Weight
from Guard G join Application A on G.CNIC = A.CNIC
where G.Guard_id = @guard_id or A.F_Name = @name or A.L_Name = @name
end

--screen 5 (Update Gaurd Info)
create procedure Update_guard
	@guardid bigint,
	@Cnic bigint, 
	@F_name varchar, 
	@L_name varchar, 
	@DOB date, 
	@Contact_num bigint, 
	@Emergency_num bigint, 
	@address varchar, 
	@weight float, 
	@height float, 
	@experience int, 
	@status bit,
	@bank_acc bigint
as
begin
update Application
set F_Name = @F_name, 
	L_Name = @L_name, 
	DOB = @DOB, 
	Contact_No = @Contact_num, 
	Emergency_No = @Emergency_num, 
	Address = @address, 
	Weight = @weight, 
	Height = @height
where CNIC = @Cnic

update Guard
set Bank_Account = @bank_acc
where Guard_id = @guardid
end

--screen 10 (Shift status)
select datename(weekday, s.Date) as day, C.Cus_name, C.Cus_id, B.Branch_name, S.Shift_D_N, 
		case 
		when S.Shift_D_N = 1 and (select count(Guard_id) from Shift_Guard SG where SG.Shift_id = S.Shift_id) < B.NOG_D then 0
		when S.Shift_D_N = 0 and (select count(Guard_id) from Shift_Guard SG where SG.Shift_id = S.Shift_id) < B.NOG_N then 0
		else 1
		end as status, 
		case
		when S.Shift_D_N = 1 then B.NOG_D - (select count(Guard_id) from Shift_Guard SG where SG.Shift_id = S.Shift_id)  
		when S.Shift_D_N = 0 then B.NOG_N - (select count(Guard_id) from Shift_Guard SG where SG.Shift_id = S.Shift_id)
		else 0
		end as gaurds_needed 
from Shifts S join Branch B on S.branch_id = B.Branch_id
	join Cust_Branch CB on B.Branch_id = CB.Branc_ID
	join Customers C on CB.Cus_ID = C.Cus_id


--screen 11 (Assign guard)
--data in the text boxses will be filled depending on which row u selected in the table from prev screen
--gaurd options:
create procedure Display_available_gaurds
	@date date,
	@guardid int,
	@shiftid int
as 
begin
select G.Guard_id, A.F_Name + ' ' + A.L_Name as Name, DATEDIFF(YEAR, A.DOB, GETDATE()), Height, Weight
from Guard G join Application A on G.CNIC = A.CNIC
where G.Guard_id not in (select SG.Guard_id from Shifts S join Shift_Guard SG on S.Shift_id = SG.Shift_id where S.Date = @date)

insert into Shift_Guard (Shift_id, Guard_id) values (@shiftid, @guardid)
end


select G.Guard_id, A.F_Name + ' ' + A.L_Name as Name, DATEDIFF(YEAR, A.DOB, GETDATE()), Height, Weight
from Guard G join Application A on G.CNIC = A.CNIC
where G.Guard_id not in (select SG.Guard_id from Shifts S join Shift_Guard SG on S.Shift_id = SG.Shift_id where S.Date = @date and S.Shift_D_N = ?)