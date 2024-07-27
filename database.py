# Database main file ..


import sqlite3
import datetime
from datetime import date, timedelta


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
    def create_s_table(cls):
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
            create table IF NOT EXISTS accounts(date_ date, profit_loss varchar2, account_figure number);
        """
        Database_common_operations.run_query(query)

    @classmethod
    def create_shopping_cart(cls):
        """
        Stores product and quantity of products added by a particular Buyer in car
        """
        query = """
            create table IF NOT EXISTS shopping_cart(buyer_email varchar2, product varcahr2, product_quantity number);
        """
        Database_common_operations.run_query(query)

    @classmethod
    def create_feedback_table(cls):
        query = """
                create table IF NOT EXISTS feedback(fname varchar2, lname varchar2, email varchar2, subject varchar2, message varchar2);
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
        Database_common_operations.create_shopping_cart()
        Database_common_operations.create_feedback_table()

    @classmethod
    def clear_all_table(cls):
        """
        Method will clear/delete all records from the table names present in the list named 'tables.'
        :return: None
        """
        tables = ['user_details', 'login', 'ids', 'login_history', 'Role', 'Product', 'Category','Supplier','Order_t','Bill', 'Warehouse_Space','Sales_Return','Purchase','Purchase_Return', 'shopping_cart', 'feedback']
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
        tables = ['user_details', 'login', 'ids', 'login_history', 'Role', 'Product', 'Category','Supplier','Order_t','Bill', 'Warehouse_Space', 'Sales_Return','Purchase','Purchase_Return', 'shopping_cart', 'feedback']
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

    data = Database_common_operations.run_query_and_return_all_data(f"select c_name from Category where c_name='{c_name}'")
    c_id = "C"+str(Database_common_operations.generate_id())

    if data:
        return #mod

    query = f"insert into Category values('{c_id}','{c_name}');"
    res = Database_common_operations.run_query(query)
    if res:
        print("Category Added!")


def add_product(p_id: str,p_name: str, purchasing_rate, weight, weight_unit: str, p_desc: str, category: str, Dimension: str, p_img: str, p_qr: str, placement_WR: str, updated_by: str, last_update_by, quantity, quantity_unit: str, fragile, lower_bound, sold_in_last_30_days, sellinng_rate):

    status = "true"
    query = f"insert into Product values('{p_id}','{p_name}',{purchasing_rate},'{weight}','{weight_unit}','{p_desc}','{category}','{Dimension}','{p_img}','{p_qr}','{placement_WR}','{updated_by}','{last_update_by}','{quantity}','{quantity_unit}','{fragile}','{lower_bound}','{sold_in_last_30_days}',{sellinng_rate}, 'null', '{status}');"
    res = Database_common_operations.run_query(query)
    if res:
        print("PRODUCT ADDED!")

def add_supplier(s_name: str, phnumber, address: str, email: str, comapany: str, p_id: str):
    s_id = "S"+str(Database_common_operations.generate_id())
    query = f"insert into Supplier values('{s_id}','{s_name}','{phnumber}','{address}','{email}','{comapany}','{p_id}');"
    res = Database_common_operations.run_query(query)
    if res:
        print("Supplier Added!")
    return s_id



def add_order(buyer_id: str, P_id: str, quantity, quantity_unit: str, Completed_: bool, date_):
    o_id = "O"+str(Database_common_operations.generate_id())
    query = f"insert into Order_t values('{o_id}','{buyer_id}','{P_id}','{quantity}','{quantity_unit}', '{Completed_}', '{date_}');"
    res = Database_common_operations.run_query(query)


    
    print("Order added!")
    # Sub inventory from warehouse 
    query = f"""
            update Product set quantity = quantity - {quantity} where P_id='{P_id}'; 
        """
    Database_common_operations.run_query(query)

    return o_id 


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


def add_user(email, user_details_name, phn_number, post, city, gender, birth, address, opt_number,state):
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
    print(id)
    print(email, user_details_name, phn_number, post, opt_number, gender, birth, address, city, state)
    query = f"""
            insert into user_details values('{id}','{email}','{user_details_name}',{phn_number}, '{post}','{opt_number}',
            '{gender}','{birth}','{address}','{city}','{state}');
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
    query1 = f"select * from user_details where email = '{email}' or user_details_name = '{user_name}';"
    res = Database_common_operations.run_query_and_return_all_data(query1)
    print(res)
    if res != []:
        print("False")
        return False
    id = add_user(email, user_name, ph_number, post, opt_number, gender, birth, address, city, state)
    # Adding login credentials to login table on sign-up.
    query = f"""
    insert into login values('{id}', '{email}', '{password}', '{post}');
    """
    Database_common_operations.run_query(query)
    Database_common_operations.login_history(id)
    print('Signed Up')
    return True


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
            #print("YESSS")
            return True
    return False



def getNumberOfEmployee():
    query = """
        select * from user_details where post="Employee";
    """
    number = Database_common_operations.run_query_and_return_all_data(query)
    return len(number)



def getEmployeeDetails(id: str):

    query = f"""
        select * from user_details where id='{id}' and post='Employee';
    """
    details = Database_common_operations.run_query_and_return_all_data(query)
    return details



def getEmployeeLoginHistory(id: str):
    query = f"""
        select * from login_history where id='{id}';
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


def getMainProductData(for_select=False):

    query = """
        select P_id, P_name, Rate, Weight, Category, Quantity, Lower_Bound, Status from Product;
    """
    if for_select:
        query = """
        select P_id, P_name, Rate, Weight, Category, Quantity, Lower_Bound from Product where S_id = 'null';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    finData = []
    for x in data:
        x = x + ('false',)
        finData.append(x)
    return finData

def getSupplierProducts(sid: str):
    query = f"""
        select P_id, P_name, Rate, Weight, Category, Quantity, Lower_Bound from Product where S_id = '{sid}';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    finData = []
    for x in data:
        x = x + ('true',)
        finData.append(x)
    return finData

def updateSupplierProducts(sid: str, pid: str):
    query1 = f"""
        update Product
        SET S_id = 'null'
        where S_id = '{sid}';
    """
    Database_common_operations.run_query(query1)
    query = f"""
        update Supplier 
        SET P_id = '{pid}'
        where S_id = '{sid}';
    """
    Database_common_operations.run_query(query)
    pids = pid.split(',')
    for p in pids:
        query2 = f"""
            UPDATE Product
            SET S_id = '{sid}'
            where P_id = '{p}'
        """
        Database_common_operations.run_query(query2)
    return print("Supplier Product Updated!")


def getProductDataForEmployee():
    query = """
        select P_id, P_name, selling_price from Product;
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
    query1 = f"""
            UPDATE Product 
            SET S_id = null
            where S_id = '{sid}'; 
    """
    Database_common_operations.run_query(query)
    Database_common_operations.run_query(query1)
    return "Supplier Removed"



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


def getBuyerDetails(id='not'):
    if id == 'not':
        query = f"""
            select id,user_details_name,phn_number from user_details where post = 'Buyer';
        """
    else:
        query = f"""
                    select * from user_details where post = 'Buyer' AND id = '{id}';
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
        selling_price = {s_rate}
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


def setOrderStatus(oid: str, status: str):
    query = f"""
        UPDATE Order_t
        SET Completed_ = '{status}'
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

"""

Sub-function - temp-not working 
def generate_bill(order_ids: list, shipping_address, payment_status):
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

    query = f""
    
        insert into Bill values('{bill_id}', {total_amount}, '{date_}', '{total_order_ids}', '{shipping_address}','{payment_status}');
    ""

    Database_common_operations.run_query(query)


"""



def add_bill(order_id: list, shipping_address, payment_status):
    bill_id = "B"+str(Database_common_operations.generate_id())
    bill_amt = 70 # Basic shipping charge
    for x in order_id:
        rate = Database_common_operations.run_query_and_return_all_data(f"select selling_price from Product where P_id == (select P_id from Order_t where Order_id = '{x}');")
        quan = Database_common_operations.run_query_and_return_all_data(f"select Quantity from Order_t where Order_id = '{x}';")
        final = int(rate[0][0])*int(quan[0][0])
        bill_amt = bill_amt+final
    date_time = str(datetime.datetime.today())[:-7]
    o_id = ""
    for y in order_id:
        if x == order_id[-1]:
            o_id += y
            break 
        
        o_id += y+","
    query = f"insert into Bill values('{bill_id}','{bill_amt}','{date_time}','{o_id}', '{shipping_address}', '{payment_status}')"
    res = Database_common_operations.run_query(query)
    if res:
        print("Bill added!")
        
    return bill_amt, bill_id



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

    for x in range(0, 7):
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



def profitLastSevenDays():
    date_= date.today()
    date_ = str(date_)
    date_ = date_.split('-')

    a_date = datetime.date(int(date_[0]), int(date_[1]), int(date_[2]))


    week_dates = []

    for x in range(1, 8):
        days = datetime.timedelta(x)
        new_date = a_date - days 
        week_dates.append(str(new_date))

    data = []
    for x in week_dates:
        temp = Database_common_operations.run_query_and_return_all_data(f"""
            select account_figure from accounts where date_ = '{x}'
        """)[0][0]

        data.append(temp)

    return week_dates, data 

    

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

# by Ohm

def deleteProduct(pid: str):
    query = f"""
    UPDATE Product Set Status = 'false' where P_id = '{pid}';
    """
    res = Database_common_operations.run_query(query)
    if res:
        return "Prodtuct_Disabled!"

def activateProduct(pid: str):
    query = f"""
    UPDATE Product Set Status = 'true' where P_id = '{pid}';
    """
    res = Database_common_operations.run_query(query)
    if res:
        return "Prodtuct_Activated!"

def getProductsforDisplay(quan=0, pid='P'):
    if quan == 0 and pid == 'P':
        query = f"""
                select P_id,P_Name,selling_price from Product where Status='true';
            """
    elif not pid == 'P':
        query = f"""
            select P_id,P_Name,selling_price from Product where P_id = '{pid}' AND Status='true';
        """
    else:
        query = f"""
            select P_id,P_Name,selling_price from Product where Status='true' LIMIT {quan};
        """
    arr = Database_common_operations.run_query_and_return_all_data(query)
    final_pro = []
    for x in arr:
        x = x + tuple(getImgpath(x[0]))
        final_pro.append(x)
    return final_pro


def getImgpath(id: str):
    query = f"""
        select P_img from Product where P_id = '{id}';
    """
    img_str = str(Database_common_operations.run_query_and_return_all_data(query)[0][0]).lstrip(',')
    img_name_arr = img_str.split(',')
    final_list = []
    for x in img_name_arr:
        final = f'/static/images/Product_img/{id}/' + x
        final_list.append(final)
    return final_list

print(getImgpath('P87'))

def getEmployee_emails():
    query = """
        select email from user_details where post = 'Employee';
    """
    res = Database_common_operations.run_query_and_return_all_data(query)
    return res


def validateEmployee(email: str, password: str, post: str):
    query = f"""
        select * from login where email_id = '{email}';
    """
    res = Database_common_operations.run_query_and_return_all_data(query)
    if email == res[0][1] and password == res[0][2] and post == res[0][3]:
        return True
    return False


def addProductInCart(email_id: str, product: str, quantity):
    query = f"""
        insert into shopping_cart values('{email_id}', '{product}', {quantity});
    """
    Database_common_operations.run_query(query)
    return "Product added in Cart"


def getNoOfItemsInCart(email: str):
    query = f"""
        select COUNT(*) from shopping_cart where buyer_email = '{email}'; 
    """
    count = Database_common_operations.run_query_and_return_all_data(query)[0][0]
    return count


def getProductsFromCart(email: str):
    query = f"""
        select product, product_quantity from shopping_cart where buyer_email = '{email}';
    """
    Data = Database_common_operations.run_query_and_return_all_data(query)
    return Data


def incQuantityInCart(email: str, pid: str):
    query1 = f"""
        select product_quantity from shopping_cart where buyer_email = '{email}' AND product = '{pid}';
    """
    query2 = f"""
            select Quantity from Product where P_id = '{pid}';
        """
    quan = Database_common_operations.run_query_and_return_all_data(query1)[0][0]
    pro_quan = Database_common_operations.run_query_and_return_all_data(query2)[0][0]
    if quan >= pro_quan:
        return print("Limit Reached")
    query = f"""
        UPDATE shopping_cart
        SET product_quantity = product_quantity + 1
        where (buyer_email = '{email}' AND product = '{pid}');  
    """
    Database_common_operations.run_query(query)
    return "QUANTITY INCREMENTED"


def decQuantityInCart(email: str, pid: str):
    query = f"""
        UPDATE shopping_cart
        SET product_quantity = product_quantity - 1
        where (buyer_email = '{email}' AND product = '{pid}');  
    """
    Database_common_operations.run_query(query)
    return "QUANTITY DECREMENTED"


def deleteProductFromCart(email: str, pid: str):
    query = f"""
        DELETE from shopping_cart where(buyer_email = '{email}' AND product = '{pid}');
    """
    Database_common_operations.run_query(query)
    return "Product Deleted!"


def check_email_avail(email):
    query = f"""

        select * from user_details where email="{email}";
    """

    data = Database_common_operations.run_query_and_return_all_data(query)

    if data:
        return False

    return True


def get_current_shipping_address(email):
    
    query = f"""
        select Address, city, state from user_details where email="{email}";
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    data = data[0]

    next_line = '\n'
    address = data[0] + next_line + data[1] + next_line + data[2]
    return address


def getBuyerName(email='none', bid='none'):
    query = f"""
        select user_details_name from user_details where email='{email}';
    """
    if bid != 'none':
        query = f"""
        select user_details_name from user_details where id='{bid}'; 
    """
    name = Database_common_operations.run_query_and_return_all_data(query)[0]

    return name



def getProductName(pid):
    query = f"""
        select P_Name from Product where P_id='{pid}'
    """

    name = Database_common_operations.run_query_and_return_all_data(query)

    return name


def getProductSellingPrice(pid):
    query = f"""
        select selling_price from Product where P_id='{pid}'
    """

    selling_price = Database_common_operations.run_query_and_return_all_data(query)

    return selling_price[0]


def getOrderHistory(email):
    query1 = f"""
            select id from user_details where email = '{email}';
        """
    bid = Database_common_operations.run_query_and_return_all_data(query1)[0][0]
    details = []

    query = f"""
        select Order_id from Order_t where Buyer_id='{bid}';
    """

    order_ids = Database_common_operations.run_query_and_return_all_data(query)

    for i in range(len(order_ids)):
        order_ids[i] = order_ids[i][0]

    # (product name, quantity, price, order_date, product image )
    
    query = f"""
        select P_id from Order_t where Buyer_id='{bid}';
    """

    pids = Database_common_operations.run_query_and_return_all_data(query)


    # Converting pids into list form list of tuples 
    for i in range(len(pids)):
        pids[i] = pids[i][0]
    
    
    # Order dates 

    query = f"""
        select Order_date from Order_t where Buyer_id ='{bid}';
    """

    order_dates = Database_common_operations.run_query_and_return_all_data(query)
    for i in range(len(order_dates)):
        order_dates[i] = order_dates[i][0]


    # Order quantity  

    query = f"""
        select Quantity from Order_t where Buyer_id ='{bid}';
    """

    product_quantity = Database_common_operations.run_query_and_return_all_data(query)
    for i in range(len(product_quantity)):
        product_quantity[i] = product_quantity[i][0]

    product_names = []
    product_images = []
    product_price = []
    product_desc = []

    for i in range(len(pids)):
        query = f"select  P_Name, P_desc, selling_price from Product where P_id='{pids[i]}'; "
        row = Database_common_operations.run_query_and_return_all_data(query)[0]
        product_desc.append(row[1])
        product_names.append(row[0])
        product_price.append(row[2])
        product_images.append(getImgpath(pids[i])[0])

    # Making final list of data 
    
    for i in range(len(pids)):
        temp = ( order_ids[i], order_dates[i], product_names[i], product_images[i], product_price[i], product_desc[i], product_quantity[i])
        details.append(temp)

    
    return details 


def getOrderStatus(order_id):
    
    query = f"""
        select Completed_, Order_date from Order_t where Order_id='{order_id}'
    """

    data = Database_common_operations.run_query_and_return_all_data(query)[0]
    order_date = data[1]
    status = data[0]

    return status, order_date

def getFilteredOrders(filter: str):
    temp = str(date.today()).split('-')
    if filter == 'monthly':
        filter_date = temp[0]+'-'+temp[1]
    elif filter == 'weekly':
        final = []
        for x in range(0,7):
            try:
                te = str(date.today() - timedelta(x))
                query = f"""
                        select Order_id from Order_t where Order_date LIKE '{te}%';
                    """
                data = Database_common_operations.run_query_and_return_all_data(query)
                final.append(data[0][0])
            except:
                pass
        return final
    elif filter == 'today':
        filter_date = date.today()
    query = f"""
        select Order_id from Order_t where Order_date LIKE '{filter_date}%';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    final = []
    for x in data:
        final.append(x[0])
    return final

def cancelOrder(oid: str):
    query = f"""
        delete from Order_t where Order_id = '{oid}';
    """
    Database_common_operations.run_query(query)
    return "Order Cancelled!"

def getOrderDetails(id: str):
    if 'O' in id:
        query = f"""
            select * from Order_t where Order_id = '{id}';
        """
    else:
        query = f"""
                    select * from Order_t where Buyer_id = '{id}';
                """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data


def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key

def getMinAndMaxProPrice():
    query1 = """
        select MIN(selling_price) from Product;
    """
    min = Database_common_operations.run_query_and_return_all_data(query1)[0][0]
    query2 = """
        select MAX(selling_price) from Product;
    """
    max = Database_common_operations.run_query_and_return_all_data(query2)[0][0]
    data = [min, max]
    return data


max_p = int(getMinAndMaxProPrice()[1])
def getFilteredProducts(category='All', price=max_p, quantity=0, company='All'):
    #Category=0 Company=0
    if category == 'All' and company == 'All':
        print('ca=0 co=0')
        query = f"""
            select P_id,P_Name,selling_price from Product where selling_price <= {price} AND Quantity >= {quantity};
        """
    elif category == 'All' and company != 'All':
        S_id = getCompanies(company)[0]
        print('ca=0 co=1')
        query = f"""
            select P_id,P_Name,selling_price from Product where selling_price <= {price} AND Quantity >= {quantity} AND S_id = '{S_id}';
        """
    elif category != 'All' and company == 'All':
        print('ca=1 co=0')
        query = f"""
            select P_id,P_Name,selling_price from Product where selling_price <= {price} AND Quantity >= {quantity} AND Category = '{category}';
        """
    else:
        S_id = getCompanies(company)[0]
        print('ca=1 co=1')
        query = f"""
            select P_id,P_Name,selling_price from Product where selling_price <= {price} AND Quantity >= {quantity} AND Category = '{category}' AND S_id = '{S_id}';
        """
    arr = Database_common_operations.run_query_and_return_all_data(query)
    final_pro = []
    for x in arr:
        x = x + tuple(getImgpath(x[0]))
        final_pro.append(x)
    return final_pro

def addFeedback(fname: str, lname: str, email: str, subject: str, message: str):
    query = f"""
        insert into feedback values('{fname}', '{lname}', '{email}', '{subject}', '{message}');
    """
    Database_common_operations.run_query(query)
    return "Feedback Added!"

def addProductSupplier(Pid: str, sid: str):
    pids = Pid.split(',')
    for pid in pids:
        query = f"""
                UPDATE Product 
                SET S_id = '{sid}'
                where P_id = '{pid}';
            """
        Database_common_operations.run_query(query)
    return "Supplier Added"

def getCompanies(company='null'):
    query = """
        select Company_name from Supplier;
    """
    if company != 'null':
        query = f"""
            select S_id from Supplier where Company_name = '{company}';
        """
    temp = Database_common_operations.run_query_and_return_all_data(query)
    data = []
    for x in temp:
        data.append(x[0])
    return data

def addProfitOrLoss():
    today_date = str(date.today())
    query1 = """
        select date_ from accounts; 
    """
    date_data = Database_common_operations.run_query_and_return_all_data(query1)
    for y in date_data:
        if str(y[0]) == today_date:
            return "Already Profit Inserted"
    orders = getAllOrdersDetails()
    PIDs = []
    for order in orders:
        data = (order[2],order[3])
        PIDs.append(data)
    CPs = []
    for C_pid in PIDs:
        Product_price_c = int(getDetailedProductsData(C_pid[0])[0][2])
        Product_quantity_c = int(C_pid[1])
        C_final = Product_price_c*Product_quantity_c
        CPs.append(C_final)

    SPs = []
    for S_pid in PIDs:
        Product_price_s = int(getDetailedProductsData(S_pid[0])[0][18])
        Product_quantity_s = int(S_pid[1])
        S_final = Product_price_s*Product_quantity_s
        SPs.append(S_final)

    Final_CP = 0
    for cp in CPs:
        Final_CP += int(cp)

    Final_SP = 0
    for sp in SPs:
        Final_SP += int(sp)

    Profit = Final_SP - Final_CP

    if Profit < 0:
        Status = 'loss'
    else:
        Status = 'profit'

    query = f"""
        insert into accounts values('{today_date}', '{Status}', {Profit});
    """
    Database_common_operations.run_query(query)
    return Profit

def getReviews(id: str):
    email = getBuyerDetails(id)[0][1]
    query = f"""
        select * from feedback where email = '{email}';
    """
    data = Database_common_operations.run_query_and_return_all_data(query)
    return data

def checkCompany(c_name: str):
    query = """
            select Company_name from Supplier;
        """
    data_t = Database_common_operations.run_query_and_return_all_data(query)
    data = []
    for x in data_t:
        data.append(x[0])
    temp1 = c_name
    for y in data:
        temp2 = str(temp1).lower()
        temp3 = str(y).lower()
        print(temp2 + '=' + temp3)
        if temp2 == temp3:
            return False
    return True

def validateCartProduct(email: str, pid: str):
    print(f"Email: {email}")
    print(f"Pid: {pid}")
    query = f"""
        select * from shopping_cart where buyer_email = '{email}' AND product = '{pid}';
    """
    res = Database_common_operations.run_query_and_return_all_data(query)
    if res:
        return True
    return False



def soldInParticularMonth(current_yr: str, month: str, pid: str):
    query = f"select COUNT(Order_id) from Order_t where Order_date LIKE '%{current_yr}-{month}%' AND P_id = '{pid}';"
    data = Database_common_operations.run_query_and_return_all_data(query)[0][0]
    return data



def updateSoldInLast(pid: str, quan):
    query = f"""UPDATE Product
    SET Sold_in_last_30_days = {quan}
    where P_id = '{pid}';
    """
    Database_common_operations.run_query(query)
    return "UPDATED!"

