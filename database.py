# Database main file ..

import sqlite3
import datetime
from datetime import date

#####################################################
#   Database common operation class
#####################################################


class Database_common_operations:
    """
        This is base class for all other database classes, This class will have all classmethods only.
    """

    @classmethod
    def run_query(cls, query: str):
        """
        This method is used to run a query.
        :param query: Must be in valid SQL syntax.
        :return: None
        """

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def run_query_and_return_all_data(cls, query):
        """
               This method is used to run a query.
               :param query: Must be in valid SQL syntax.
               :return: None
               """

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return data

    @classmethod
    def create_userDetails_table(cls):
        """
        Creates user table.
        :return: None
        """

        query = f"""
            create table user_details(id varchar2 PRIMARY KEY, email varchar2, user_details_name varchar2, phn_number number(10), post varchar2, opt_phnumber number(10), Gender varchar2, B_Date DATE, Address varchar2, FOREIGN KEY(post) REFERENCES Role(Role_Name) ON DELETE CASCADE);
        """
        Database_common_operations.run_query(query)

    @classmethod
    def create_login_table(cls):
        """
        This method will create a new login table.
        login table stores login credentials of all the users.
        :return: None
        """
        query = f"""
            create table IF NOT EXISTS login (ID varchar2,email_id varchar2, password varchar2, post varchar2, FOREIGN KEY(ID) REFERENCES user_details(ID) ON DELETE CASCADE) ;
        """
        cls.run_query(query)

    @classmethod
    def create_role_table(cls):
        """
        This method will create a new Role table.
        Role table describes different types of roles available in the System.
        return: None
        """
        query = f"""
            create table  IF NOT EXISTS Role (Role_Name varchar2 PRIMARY KEY);
        """
        cls.run_query(query)

    
    @classmethod
    def create_product_table(cls):
        query = "create table IF NOT EXISTS Product (P_id varchar2 PRIMARY KEY, P_Name varchar2, Rate DOUBLE, Weight DOUBLE, Weight_Unit varchar2, P_desc varchar2, Category varchar2, Dimension varchar2, P_img varchar2, p_qr_code varchar2, PlacementInWarehouse varchar2, Updated_by varchar2, Last_updating_date DATE, Quantity number, Quantity_Unit varchar2, Fragile BOOLEAN, Lower_Bound number, Sold_in_last_30_days number, FOREIGN KEY(Category) REFERENCES Category(Category_Name) ON DELETE CASCADE);"
        res = cls.run_query(query)
        if res:
            print("Product table created")

    @classmethod
    def create_category_table(cls):
        query = "create table IF NOT EXISTS Category (Category_id varchar2 PRIMARY KEY, Category_Name varchar2);"
        res = cls.run_query(query)
        if res:
            print("Category table created")

    @classmethod
    def create_supplier_table(cls):
        query = f"create table IF NOT EXISTS Supplier (S_id varchar2 PRIMARY KEY, S_Name varchar2, PhNumber number, Address varchar2, Email varchar2, Company_name varchar2, P_id varchar2);"
        res = Database_common_operations.run_query(query)
        if res:
            print("SUPPLIER CREATED")

    @classmethod
    def create_order_table(cls):
        query = f"create table IF NOT EXISTS Order_t (Order_id varchar2 PRIMARY KEY, Buyer_id, P_id varchar2, Quantity number, Quantity_unit varchar2,  Completed_  BOOLEAN, FOREIGN KEY(P_id) REFERENCES Product(P_id));"
        res = Database_common_operations.run_query(query)
        if res:
            print("Order Table Created!")

    @classmethod
    def create_bill_table(cls):
        query = """create table IF NOT EXISTS Bill (Bill_id varchar2 PRIMARY KEY, 
        Bill_amt number, Date_Time DATE, Order_id varchar2);"""
        res = Database_common_operations.run_query(query)
        if res:
            print("Bill Table Created!")

    @classmethod
    def create_warehouse_space_table(cls):
        query = """create table IF NOT EXISTS Warehouse_Space (Location_id varchar2 PRIMARY KEY, 
        Is_empty BOOLEAN, P_id varchar2, L_Dimensions varchar2, 
        For_fragile BOOLEAN, FOREIGN KEY(P_id) REFERENCES Product(P_id));"""
        res = Database_common_operations.run_query(query)
        if res:
            print("Bill Table Created!")

    @classmethod
    def create_sales_return_table(cls):
        query = """create table IF NOT EXISTS Sales_Return (Return_id varchar2 PRIMARY KEY,
         Bill_id varchar2, Quantity_Return number, 
         Order_id varchar2, FOREIGN KEY(Bill_id) REFERENCES Bill(Bill_id));"""
        res = Database_common_operations.run_query(query)
        if res:
            print("Sales Return Table Created!")

    @classmethod
    def create_purchase_table(cls):
        query = """create table IF NOT EXISTS Purchase (Purchase_id varchar2, 
        P_id varchar2, Quantity number, Amount number, S_id varchar2, 
        Date_Time DATE, FOREIGN KEY(P_id) REFERENCES Product(P_id));"""
        res = Database_common_operations.run_query(query)
        if res:
            print("Purchase Table Created!")

    @classmethod
    def create_purchase_return(cls):
        query = """create table IF NOT EXISTS Purchase_Return(P_return_id varchar2 PRIMARY KEY,
             Purchase_id varchar2, FOREIGN KEY(Purchase_id) REFERENCES Purchase(Purchase_id)
             );"""
        res = Database_common_operations.run_query(query)
        if res:
            print("Purchase Return Table Created!")

    @classmethod
    def create_id_table(cls):
        """
        This method creates a new id table.
        Id table is used to auto-generate new id for a new user, employee or user_details.
        :return:
        """
        query = f"""
                    create table  IF NOT EXISTS ids (id number);
                """
        cls.run_query(query)

        add_first_id = f"""
                           insert into ids values(1);
                       """
        cls.run_query(add_first_id)

    @classmethod
    def generate_id(cls):
        """
        This method gets previously generated id from the database table 'ids' and increments that id by one and stores
        the new id into the table.


        :return: new id (datatype: number)
        """
        query = """
            select id from ids;
        """
        previous_id = cls.run_query_and_return_all_data(query)
        next_id = previous_id[0][0] + 1
        query = f"""
            update ids set id={next_id} where id={previous_id[0][0]}
        """
        cls.run_query(query)
        return next_id

    @classmethod
    def create_accounts_table(cls):
        """
        Stores Profit and loss of the warehouse for each day it has a day ending profit figure
        """

        query = """
            create table accounts(date_ date, profit_loss varchar2, account_figure number);
        """
        Database_common_operations.run_query(query)

    
    @classmethod
    def create_all_tables(cls):
        Database_common_operations.create_role_table()
        Database_common_operations.create_userDetails_table()
        Database_common_operations.create_id_table()
        Database_common_operations.create_login_table()
        Database_common_operations.create_login_history_table()
        Database_common_operations.create_category_table()
        Database_common_operations.create_product_table()
        Database_common_operations.create_order_table()
        Database_common_operations.create_supplier_table()
        Database_common_operations.create_bill_table()
        Database_common_operations.create_warehouse_space_table()
        Database_common_operations.create_sales_return_table()
        Database_common_operations.create_purchase_table()
        Database_common_operations.create_purchase_return()

    @classmethod
    def clear_all_table(cls):
        """
        Method will clear/delete all records from the table names present in the list named 'tables.'
        :return: None
        """
        tables = ['user_details', 'login', 'ids', 'login_history', 'Role', 'Product', 'Category','Supplier','Order_t','Bill', 'Warehouse_Space','Sales_Return','Purchase','Purchase_Return']
        for table in tables:
            query = f"delete from {table}"
            cls.run_query(query)
            print("CLEARED")
        return "CLEARED"

    @classmethod
    def drop_all_table(cls):
        """
        Method will Drop/Destroy all the tables names present in the list named 'tables.'
        :return: None
        """
        tables = ['user_details', 'login', 'ids', 'login_history', 'Role', 'Product', 'Category','Supplier','Order_t','Bill', 'Warehouse_Space', 'Sales_Return','Purchase','Purchase_Return']
        for table in tables:
            query = f"DROP TABLE {table}"
            cls.run_query(query)
            print("DROPPED")



    @classmethod
    def create_login_history_table(cls):
        """
        This method creates new login history table, this table will be used to store login date and time of users.

        :return:
        """
        query = f"""
        create table login_history(id varchar2, date varchar2, time varchar2);
        """
        Database_common_operations.run_query(query)

    @classmethod
    def login_history(cls, id):
        """
        Save the login date and time of the user!
        :param id: Id of the user who has logged-in.
        :return: None
        """
        date_time = str(datetime.datetime.today())[:-7]
        print(date_time)
        time = date_time[11:]
        date = date_time[:10]
        query = f"""
                insert into login_history values('{id}','{date}','{time}')
                """
        Database_common_operations.run_query(query)





#####################################################
#   User Details class
#####################################################

def add_role(role_name: str):
    """
    Add type of role
    :return: None
    """
    tmp = role_name
    query = f"""
        insert into Role values('{tmp}');   
    """
    Database_common_operations.run_query(query)
    if query:
        print("Role Added")



def add_category(c_name: str):
    c_id = "C"+str(Database_common_operations.generate_id())
    query = f"insert into Category values('{c_id}','{c_name}');"
    res = Database_common_operations.run_query(query)
    if res:
        print("Category Added!")

def add_product(p_id: str,p_name: str, purchasing_rate, weight, weight_unit: str, p_desc: str, category: str, Dimension: str, p_img: str, p_qr: str, placement_WR: str, updated_by: str, last_update_by, quantity, quantity_unit: str, fragile, lower_bound, sold_in_last_30_days, sellinng_rate):
    query = f"insert into Product values('{p_id}','{p_name}',{purchasing_rate},'{weight}','{weight_unit}','{p_desc}','{category}','{Dimension}','{p_img}','{p_qr}','{placement_WR}','{updated_by}','{last_update_by}','{quantity}','{quantity_unit}','{fragile}','{lower_bound}','{sold_in_last_30_days}',{sellinng_rate});"
    res = Database_common_operations.run_query(query)
    if res:
        print("PRODUCT ADDED!")

def add_supplier(s_name: str, phnumber, address: str, email: str, comapany: str, p_id: str):
    s_id = "S"+str(Database_common_operations.generate_id())
    query = f"insert into Supplier values('{s_id}','{s_name}','{phnumber}','{address}','{email}','{comapany}','{p_id}');"
    res = Database_common_operations.run_query(query)
    if res:
        print("Supplier Added!")



def add_order(buyer_id: str, P_id: str, quantity, quantity_unit: str, Completed_: bool):
    o_id = "O"+str(Database_common_operations.generate_id())
    query = f"insert into Order_t values('{o_id}','{buyer_id}','{P_id}','{quantity}','{quantity_unit}', '{Completed_}');"
    res = Database_common_operations.run_query(query)
    if res:
        print("Order added!")



def add_bill(order_id):
    bill_id = "B"+str(Database_common_operations.generate_id())
    bill_amt = 0
    for x in order_id:
        rate = Database_common_operations.run_query_and_return_all_data(f"select Rate from Product where P_id == (select P_id from Order_t where Order_id == {x});")
        quan = Database_common_operations.run_query_and_return_all_data(f"select Quantity from Order_t where Order_id == {x};")
        final = int(rate[0][0])*int(quan[0][0])
        bill_amt = bill_amt+final
    date_time = str(datetime.datetime.today())[:-7]
    o_id = ""
    for y in order_id:
        o_id += y+","
    query = f"insert into Bill values('{bill_id}','{bill_amt}','{date_time}','{o_id}')"
    res = Database_common_operations.run_query(query)
    if res:
        print("Bill added!")

def add_warehouse_space(is_empty: bool, p_id: str, l_dimension: str, for_fragile: bool):
    l_id = "L"+str(Database_common_operations.generate_id())
    query = f"insert into Warehouse_Space values('{l_id}','{is_empty}','{p_id}','{l_dimension}','{for_fragile}');"
    res = Database_common_operations.run_query(query)
    if res:
        print("Space added!")

def add_sales_return(bill_id: str, quan_return, order_id: str):
    r_id = "R"+str(Database_common_operations.generate_id())
    bill_id_arr = Database_common_operations.run_query_and_return_all_data("select Bill_id from Bill;")
    flag = 0
    for x in bill_id_arr:
        if bill_id == str(x[0][0]):
            flag += 1
    if flag == 0:
        return "Bill Not Exists!"
    orders = Database_common_operations.run_query_and_return_all_data(f"select Order_id from Bill where Bill_id == {bill_id};")
    temp = str(orders[0][0])
    index = temp.find(order_id)
    if index<0:
        return "Order Not Exists!"
    order_quan = Database_common_operations.run_query_and_return_all_data(f"select Quantity from Order_t where Order_id == {order_id};")
    temp1 = int(order_quan[0][0])
    if quan_return>temp1:
        return "Retrun Quantity Exceeds than actual purchased quantity"
    query = f"insert into Sales_Return values('{r_id}','{bill_id}','{quan_return}','{order_id}');"
    res = Database_common_operations.run_query(query)
    if res:
        return "Returned Successfully!"

def add_purchase(p_id: str, quantity, amount, s_id: str):
    pur_id = "Pur"+str(Database_common_operations.generate_id())
    p_id_arr = Database_common_operations.run_query_and_return_all_data("select P_id from Product;")
    flag = 0
    for x in p_id_arr:
        if p_id == str(x[0][0]):
            flag += 1
    if flag == 0:
        return "No Product Exists!!"
    old_quan_arr = Database_common_operations.run_query_and_return_all_data(f"select Quantity from Product where P_id == {p_id};")
    old_quan = float(old_quan_arr[0][0])
    final = old_quan+float(quantity)
    query1 = f"UPDATE Product set Quantity = {final} where P_id == {p_id};"
    res1 = Database_common_operations.run_query(query1)
    if res1:
        print("Product incremented!")
    s_id_arr = Database_common_operations.run_query_and_return_all_data("select S_id from Supplier;")
    flag1 = 0
    for y in s_id_arr:
        if s_id == str(y[0][0]):
            flag1 += 1
    if flag1 == 0:
        return "No Supplier Exists!!"
    date_time = str(datetime.datetime.today())[:-7]
    query2 = f"insert into Purchase values('{pur_id}','{p_id}','{quantity}','{amount}','{s_id}','{date_time}');"
    res = Database_common_operations.run_query(query2)
    if res:
        return "Purchased Successfully!"

def add_purchase_return(pur_id: str, quan_ret):
    p_ret_id = "pur_ret"+str(Database_common_operations.generate_id())
    pur_id_arr = Database_common_operations.run_query_and_return_all_data("select Purchase_id from Purchase;")
    flag = 0
    for x in pur_id_arr:
        if pur_id == str(x[0][0]):
            flag += 1
    if flag == 0:
        return "No Purchase Exists!!"
    p_id_arr = Database_common_operations.run_query_and_return_all_data(f"select P_id from Purchase where Purchase_id == (select Purchase_id from Purchase_return where Purchase_id == {pur_id});")
    p_id = str(p_id_arr[0][0])
    old_quan_arr = Database_common_operations.run_query_and_return_all_data(
        f"select Quantity from Product where P_id == {p_id};")
    old_quan = float(old_quan_arr[0][0])
    final = old_quan - float(quan_ret)
    query1 = f"UPDATE Product set Quantity = {final} where P_id == {p_id};"
    res1 = Database_common_operations.run_query(query1)
    if res1:
        print("Product decremented!")
    act_amt_arr = Database_common_operations.run_query_and_return_all_data(f"select Amount from Purchase where Purchase_id == {pur_id}")
    act_amt = int(act_amt_arr[0][0])
    final1 = float(act_amt*quan_ret)
    query = f"insert into Purchase_Return('{p_ret_id}','{pur_id}','{quan_ret}','{final1}')"
    res = Database_common_operations.run_query(query)
    if res:
        return "Purchase Returned Successfully!"


def add_category(c_name: str):
    c_id = "C"+str(Database_common_operations.generate_id())
    query = f"insert into Category values('{c_id}','{c_name}');"
    res = Database_common_operations.run_query(query)
    if res:
        print("Category Added!")



def add_user(email, user_details_name, phn_number, post, opt_number, gender, birth, address,city,state):
    """
    This method adds new user_details to the user_details table.
    :param id: str - Unique userid of the user_details.
    :param email: str - Email-id to get otp or other related information.
    :param user_details_name: str
    :param phn_number: must be a Number
    :return: None
    """
    if post == 'Admin':
        id = 'A'+str(Database_common_operations.generate_id())
    if post == 'Employee':
        id = 'E'+str(Database_common_operations.generate_id())
    if post == 'Buyer':
        id = 'B'+str(Database_common_operations.generate_id())

    query = f"""
        insert into user_details values('{id}','{email}','{user_details_name}',{phn_number}, '{post}',{opt_number},'{gender}','{birth}','{address}','{city}','{state}');
    """
    Database_common_operations.run_query(query)
    print('user_details added successfully')
    return id


def remove_user(id: str):
    """
    Removes existing user_details.
    :param id: id of the user_details who is to be removed.
    :return:
    """

    query = f"""
    delete from user_details where id = '{id}';
    """

    Database_common_operations.run_query(query)
    print('user_details removed successfully')


def edit_email(id: str, New_email):
    """
    Edits email for existing user.
    :param id: ID of the user_details who has to update his email.
    :param New_email: New email address.
    :return:
    """

    query = f"""
    update user_details
    set email = '{New_email}'
    where id = '{id}';
    """
    Database_common_operations.run_query(query)
    print('email edited successfullly')


def edit_username(id: str, new_user_name):
    """
    Edits user name.
    :param id: Id of the user who has to update his name
    :param New_user_name: updated name
    :return:
    """

    query = f"""
    update user_details
    set user_name = '{new_user_name}'
    where id='{id}';
    """
    Database_common_operations.run_query(query)
    print('user_name edited successfullly')


def edit_phn_number(id: str, New_phn_number):
    """
    Edits user mobile number.
    :param id: Id of the user who has to update his phone number.
    :param New_phn_number: updated phone number of the user.
    :return:
    """

    query = f"""
    update user_details
    set phn_number = {New_phn_number}
    where id = '{id}';
    """
    Database_common_operations.run_query(query)
    print('phn_number edited successfully')


def sign_up(email: str, user_name: str, ph_number, password: str, post: str, gender: str, birth: str, address: str, city: str, state: str,opt_number = 0):
    """
    Sign's up new user.
    :param email: Valid email address of the user.
    :param user_name:  Name of the user.
    :param phn_number:  Phone number of the user.
    :param password:    password of the user.
    :return: None
    """
    if not opt_number:
        opt_number = 0 

    id = add_user(email, user_name, ph_number, post,opt_number, gender, birth, address, city, state)
    # Adding login credentials to login table on sign-up.
    query = f"""
    insert into login values('{id}', '{email}', '{password}', '{post}');
    """
    Database_common_operations.run_query(query)
    Database_common_operations.login_history(id)
    print('Signed Up')


def validate_login(email_id, password, post):
    query = f"""
            select * from login where email_id='{email_id}' and password='{password}'; 
        """
    valid_details = Database_common_operations.run_query_and_return_all_data(query)
    query = f"""
            select * from login where post='{post}';
        """
    valid_post = Database_common_operations.run_query_and_return_all_data(query)

    if valid_details:
        if valid_post:
            # Adding log-in activity to login_history table

            # Selecting id of user

            query = f"""
                    select id from login where email_id='{email_id}';
                """
            id = Database_common_operations.run_query_and_return_all_data(query)[0][0]
            Database_common_operations.login_history(id)
            print("YESSS")
            return True
    return False



def getNumberOfEmployee():
    query = """
        select * from user_details where post="Employee";
    """
    number = Database_common_operations.run_query_and_return_all_data(query)
    return len(number)



def getEmployeeDetails(str: id):

    query = f"""
        select * from user_details where id='{id}' and post='Employee';
    """
    details = Database_common_operations.run_query_and_return_all_data(query)
    return details



def getEmployeeLoginHistory(str: id):
    query = f"""
        select * from login_history where id={id}
    """
    details = Database_common_operations.run_query_and_return_all_data(query)
    return details



def employeeProductUpdateHistory(id):
    query = f"""
        select Updated_by, Last_updating_date from Product where Updated_by='{id}';
    """

    data = Database_common_operations.run_query_and_return_all_data(query)
    return data 


def getDetailedProductsData(P_id):
    
    query = f"""
        select * from Product where P_id='{P_id}';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data 


def getMainProductData():

    query = f"""
        select P_id, P_name, Rate, Weight, Category, Quantity, Lower_Bound from Product;
        
    """

    data = Database_common_operations.run_query_and_return_all_data(query)
    return data


def getNumberOfProducts():
    query = f"""
        select * from Product;
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return len(data)


def getNumberOfPendingOrders():
    query = f"""
        select * from Order_t where Completed_='false';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return len(data)


def getNumberOfSupplier():
    query = """
        select * from Supplier    
    """

    data = Database_common_operations.run_query_and_return_all_data(query)
    return len(data)


def getAllSuppliers():
    query = """
        select * from Supplier
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data


def removeSupplier(sid):
    query = f"""
        delete from Supplier where S_id='{sid}'
    """
    Database_common_operations.run_query(query)


def getLowerBoundProducts():

    query = f"""
        select P_id, P_name, Quantity, Lower_Bound from Product where Quantity < Lower_Bound;
    """

    data = Database_common_operations.run_query_and_return_all_data(query)
    return data 



def addProductInventory(quantity, pid):
    query = f"""
    update Product set Quantity = Quantity + {quantity} where P_id='{pid}';
    """
    Database_common_operations.run_query(query)



def subProductInventory(quantity,pid):
    query = f"""
        update Product set Quantity = Quantity - {quantity} where P_id='{pid}';
    """
    Database_common_operations.run_query(query)


def editProductInventory(quantity, operation, pid):

    if operation == 'add':
        addProductInventory(quantity, pid)
    else:
        subProductInventory(quantity, pid)


def getAdminDetails(admin_name): # your_details 
    query = f"""
        select * from user_details where user_details_name = '{admin_name}';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data 


def getAdminID(admin_name):
    query = f"""                    
        select id from user_details where user_details_name = '{admin_name}';
    """
    id = Database_common_operations.run_query_and_return_all_data(query)
    return id 


def getAdminLoginHistory(id):
    query = f"""
        select date, time from login_history where id = '{id}';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data 



def getAdminLoginDetails(id):
    query = f"""
        select * from login where ID = '{id}'
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data 


def getAllOrdersDetails():
    query = """
        select * from Order_t;
    """

    data = Database_common_operations.run_query_and_return_all_data(query)
    return data


def getBuyerDetails():
    query = f"""
        select id,user_details_name,phn_number from user_details where post = 'Buyer';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data


def getFullfilledOrders():
    query = """
        select * from Order_t where Completed_= 'true';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data


def edit_product_details(id, p_name: str, p_rate, s_rate, weight, w_unit: str, desc: str, cate: str, dimen: str, placement: str, lower_bound):
    query = f"""
        UPDATE Product
        SET P_Name = '{p_name}', Rate = '{p_rate}', Weight = '{weight}', Weight_Unit = '{w_unit}', P_desc = '{desc}', 
        Category = '{cate}', Dimension = '{dimen}', PlacementInWarehouse = '{placement}', Lower_Bound = '{lower_bound}', 
        Selling_Rate = {s_rate}
        where P_id = '{id}';
    """
    res = Database_common_operations.run_query(query)
    if res:
        return "Product updated!"


def getCategory():
    query = """
        select Category_Name from Category;
    """
    category = Database_common_operations.run_query_and_return_all_data(query)
    return category


def setOrderFullfill(oid: str):
    query = f"""
        UPDATE Order_t
        SET Completed_ = 'true'
        where Order_id = '{oid}';
    """
    res = Database_common_operations.run_query(query)
    if res:
        print("Order Completed!")


def unsetOrderFullfill(oid: str):
    query = f"""
        UPDATE Order_t
        SET Completed_ = 'false'
        where Order_id = '{oid}';
    """
    res = Database_common_operations.run_query(query)
    if res:
        print("Order Completed!")


def remove_product(pid: str):
    query = f"""
        delete from Product where P_id = '{pid}';
    """
    res = Database_common_operations.run_query(query)
    if res:
        print("Product Deleted!")


def updatePassword(email_id, new_password):
    query = f"""
        update login set password='{new_password}' where email_id='{email_id}';
    """

    Database_common_operations.run_query(query)


def getOrderAmount(order_id):
    query = f"""
        select selling_price from Product where P_id in 
        (select P_id from Order_t where Order_id = '{order_id}');
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data[0][0]


def generate_bill(order_ids: list):
    # Order ids can be multiple therefore are csv values: (- seperated values) in a single field
    
    bill_id = "Bill" + str(Database_common_operations.generate_id())


    # billing amount will be the total price of orders
    amounts = []
    for order_id in order_ids:
        amounts.append(int(getOrderAmount(order_id)))

    # Get Total bill value 
    total_amount = 0
    for x in amounts:
        total_amount += x
    
    date_ = str(date.today())
    

    # Making string type list of order_ids 
    total_order_ids = ""
    for x in order_ids:

        # If last order_id no need to add '-':
        if x == order_ids[-1]:
            total_order_ids += str(x)
            break

        total_order_ids += str(x)
        total_order_ids += '-' # seperation character 

    # Query to add the bill record

    query = f"""
    
        insert into Bill values('{bill_id}', {total_amount}, '{date_}', '{total_order_ids}');
    """

    Database_common_operations.run_query(query)
    


def totalOrdersInMonth(month_name: int):
    
    query = f"""
        select * from Order_t where Order_id in
         ( select Order_id from Bill where Date_Time like '%-{month_name}-%' )
    """
    
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data 



def totalOrdersToday():

    date_ = str(date.today())

    query = f"""
        select * from Order_t where Order_id in
         ( select Order_id from Bill where Date_Time = '{date_}' )
    """
    
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data 


def totalOrdersOnDate(date):

    query = f"""
        select * from Order_t where Order_id in
         ( select Order_id from Bill where Date_Time = '{date}' )
    """
    
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data



# New 

def orders_last_seven_days():
    """
    Returns key:value --> date: sum(order_ids)
    """
    date_= date.today()
    date_ = str(date_)
    date_ = date_.split('-')

    a_date = datetime.date(int(date_[0]), int(date_[1]), int(date_[2]))


    week_dates = []

    for x in range(1, 8):
        days = datetime.timedelta(x)
        new_date = a_date - days 
        week_dates.append(str(new_date))

    data  = {}

    for x in week_dates: # Finding sum of orders for each date 

        query = f"""
            select count(Order_id) from Order_t where Order_date = '{x}'
        """
        
        order_number = Database_common_operations.run_query_and_return_all_data(query)[0][0]

        data[f'{x}'] = order_number 

    return data 


def profitToday():

    """
        Billing Formula:
        
        profit = Bill value - [selling price of each product in list of orders * quantity purchased]
    """

    # Total number of orders 

    date_ = str(date.today())
    query = f"""
        select Order_id from Bill where Date_Time = '{date_}';
    """
    
    order_ids = Database_common_operations.run_query_and_return_all_data(query)
    # Finding cost of the product
   
    order_ids = list(order_ids[0])
    
    total_order_ids = []
    for x in order_ids:
        temp = x.split('-')
        for y in temp:
            total_order_ids.append(y)
    
    # cost = pid[selling price] * order[quantity]

    cost_price = 0
    for x in total_order_ids:
        
        query = f"select Quantity from Order_t where Order_id = '{x}' "
        quantity = Database_common_operations.run_query_and_return_all_data(query)[0][0]
        quantity = int(quantity)

        query = f"select Rate from Product where P_id in (select P_id from Order_t where Order_id = '{x}') "
        rate = Database_common_operations.run_query_and_return_all_data(query)[0][0]
        rate = int(rate)
        cost_price += quantity * rate 

    # Finding selling prices... [Total billing value]
     
    query = f"select sum(Bill_amt) from Bill where Date_time = '{date_}' "
    sales = Database_common_operations.run_query_and_return_all_data(query)[0][0]
    sales = int(sales)

    profit = sales - cost_price

    if profit > 0:
        return True, profit         # Profit 
    
    return False, profit   # Loss
    