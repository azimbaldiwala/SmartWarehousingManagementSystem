

from datetime import datetime, timedelta

from flask import Flask, render_template, request, flash, session, redirect, send_file

import database
import os
from werkzeug.utils import secure_filename
import generate_qrcode 
import sendOtp
import drawGraphs   
import validateCard
import makePayment
import generateBill
import datetime
import generateBillPdf




app = Flask(__name__)
SERVER_NAME_ = 'localhost:5050'
app.secret_key = "HX5I09WBDSDF"


@app.route('/')
def select_post():
    temp_arr = database.getProductsforDisplay(6)
    try:
        p1 = temp_arr[0]
    except:
        p1 = ['no_id','NO PRODUCT', '0000', 'static/images/NO_PRODUCT.png']
    try:
        p2 = temp_arr[1]
    except:
        p2 = ['no_id','NO PRODUCT', '0000', 'static/images/NO_PRODUCT.png']
    try:
        p3 = temp_arr[2]
    except:
        p3 = ['no_id','NO PRODUCT', '0000', 'static/images/NO_PRODUCT.png']
    try:
        p4 = temp_arr[3]
    except:
        p4 = ['no_id','NO PRODUCT', '0000', 'static/images/NO_PRODUCT.png']
    try:
        p5 = temp_arr[4]
    except:
        p5 = ['no_id','NO PRODUCT', '0000', 'static/images/NO_PRODUCT.png']
    try:
        p6 = temp_arr[5]
    except:
        p6 = ['no_id','NO PRODUCT', '0000', 'static/images/NO_PRODUCT.png']
    if 'Buyer' not in session:
        login = "false"
    else:
        login = "true"
    
    R_Data = database.Database_common_operations.run_query_and_return_all_data("select * from feedback;")
    return render_template('index.html', P1=p1, P2=p2, P3=p3, P4=p4, P5=p5, P6=p6, login=login, R_data=R_Data)


#####################################################
#   Admin login, validation and logout 
#####################################################

@app.route('/admin_login')
def admin_home():
    return render_template('admin_login.html')

@app.route('/single_product/<string:pid>')
def single_product(pid):
    if 'Buyer' not in session:
        login = "false"
    else:
        login = "true"
    img_paths = database.getImgpath(pid)
    data = database.getDetailedProductsData(pid)
    query = f"select Company_name from Supplier where S_id = '{data[0][19]}'"
    try:
        company = database.Database_common_operations.run_query_and_return_all_data(query)[0][0]
    except:
        company = 'None'
    return render_template('property-single.html', imgs=img_paths, data=data, login=login, company=company)

@app.route('/admin_login_validation', methods=["GET", "POST"])
def admin_login_validate():
    email = request.form['email']
    password = request.form['psw']
    post = 'Admin'
    is_valid = database.validate_login(email, password, post)
    query = database.Database_common_operations.run_query_and_return_all_data(
        f"select user_details_name from user_details where email == '{email}';")
    global name
    name = query[0][0]
    if is_valid:
        global numEmp
        session['Admin'] = name
        data = database.Database_common_operations.run_query_and_return_all_data("select P_id from Product;")
        for x in data: 
            current_yr = str(datetime.datetime.today())[:4]
            current_month = str(datetime.datetime.today())[5:-19]
            quan = database.soldInParticularMonth(current_yr,current_month,x[0])
            database.updateSoldInLast(x[0],quan)
        return redirect('/admin_home')
    flash("email/password is incorrect!")
    return redirect('/admin_login')


# Fogot PAssword 
@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


@app.route('/forgot_password_reponse', methods=["GET", "POST"])
def forgot_password_reponse():
    email = request.form['email']
    session['reset_password_email'] = email
    otp = sendOtp.sendOtp(email)
    session['otp'] = otp
    return render_template('forgot_password_response.html')

@app.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    otp = request.form['otp']
    if session['otp'] != otp:
        return redirect('/forgot_password')
    new_password = request.form['psw']
    new_password_conn = request.form['psw_con']

    if new_password != new_password_conn:
        return redirect('/forgot_password')

    database.updatePassword(session['reset_password_email'], new_password)
    session.pop('reset_password_email', None)
    session.pop('otp', None)
    return redirect('/admin_login')



@app.route('/logout')
def logout():
    # Session unset 
    session.pop("Admin", None)
    return render_template('admin_login.html')



#####################################################
#   Admin Panel Operations
#####################################################



@app.route('/admin_home')
def admin_login():
    
    if not 'Admin' in session:
        return redirect('/admin_login')

    numEmp_ = database.getNumberOfEmployee()
    NumberOfProducts_ = database.getNumberOfProducts()
    NumberOfOrders_ = database.getNumberOfPendingOrders()
    NumberOfSuppliers_ = database.getNumberOfSupplier()
    numberOfLowerBoundProducts = database.getLowerBoundProducts()
    graph_dataset = database.orders_last_seven_days()
    labels, values = drawGraphs.LineGraphDataset(graph_dataset)
    
    #Values just for demo 
    #values = [100,180, 300, 250, 400, 395, 500]

    labels1 = ['Month Profit', 'Week Profit', 'Todays Profit']
    # Values2 must be comming from  the database ..
    values1 = [1000000, 300000, 50000]

    labels1, values1 = database.profitLastSevenDays()

    # By default profit graph

    

    return render_template('admin_home.html', NAME=session['Admin'], 
        NumberOfEmployee=numEmp_, NumberOfProducts=NumberOfProducts_, 
        NumberOfOrder=NumberOfOrders_, NumberOfSuppliers=NumberOfSuppliers_, 
        data=numberOfLowerBoundProducts, labels=labels, values=values,
        labels1=labels1, values1=values1)



@app.route('/Sign_up_Employee')
def sign_up_Employee():
    return render_template('employee_signup.html')

@app.route('/Manage_Employees')
def Manage_Employees():

    if not 'Admin' in session:  
        return redirect('/admin_login')

    arr = database.Database_common_operations.run_query_and_return_all_data(
        "select * from user_details where post == 'Employee';")
    te = 0
    temp = []
    for x in arr:
        ID = arr[te][0]
        Ename = arr[te][2]
        PhNumber = arr[te][3]
        ar = [ID, Ename, PhNumber]
        temp.append(ar)
        te += 1

    return render_template('Manage_Employees.html', ARRAY=temp, length=te - 1, NAME=session['Admin'])



@app.route('/add_new_employee', methods=["GET", "POST"])
def add_new_employee():

    if not 'Admin' in session:
        return redirect('/admin_login')
    
    email_c = request.form['Email']
    f_name = request.form['fname']
    ph_number = request.form['PhNumber']
    PSWT = request.form['pswt']
    PSW = request.form['psw']
    POST = 'Employee'
    if PSWT == PSW:
        PASS = PSW
    else:
        print(PSW)
        print(PSWT)
        return redirect('/Sign_up_Employee')
    opt_number = request.form['PhNumber2']
    Gender = request.form['Gender']
    B_date = request.form['DOB']
    print(B_date)
    Address = request.form['Address']
    State = request.form['countrya']
    City = request.form['district']
    res = database.sign_up(email_c, f_name, ph_number, PASS, POST, Gender, B_date, Address, opt_number, City, State)
    if not res:
        flash("User Already Registered!")
        return redirect('/Sign_up_Employee')
    return redirect('/Manage_Employees')

"""
Product related operations 
"""


@app.route('/edit_product_inventory_employee/<string:pid>', methods=["GET", "POST"])
def edit_product_inventory_employee(pid):
    if not 'Employee' in session:
        return redirect('/buyer_login')
    return render_template('edit_product_inventory_employee.html', PID = pid)


@app.route('/edit_product_inventory/<string:pid>', methods=["GET", "POST"])
def edit_product_inventory(pid):
    if not 'Admin' in session:
        return redirect('/admin_login')
    return render_template('edit_product_inventory.html',PID = pid)


@app.route('/add_product')
def add_product():
    category = database.getCategory()
    tempc = []
    for x in category:
        tempc.append(x[0])
    return render_template('add_product.html', category=category, NAME=session['Admin'])


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image():
    return render_template('index.html')

@app.route('/add_new_product', methods=["GET", "POST"])
def add_new_product():
    if not 'Admin' in session:
        return redirect('/admin_login')
    p_id = "P" + str(database.Database_common_operations.generate_id())
    p_name = request.form['P_Name']
    p_rate = request.form['P_Rate']
    s_rate = request.form['S_Rate']
    weight = request.form['Weight']
    w_unit = request.form['w_unit']
    category = request.form['cate']
    fragile = request.form['Fragile']
    placement = request.form['Placement_In_Warehouse']
    quantity = request.form['quantity']
    min_quan = request.form['min_quantity']
    p_desc = request.form['p_desc']
    Dimension = request.form['Dimension']
    quan_unit = request.form['quantity_unit']
    temp = database.getCategory()
    tempc = []
    for x in temp:
        tempc.append(x[0])
    if category not in tempc:
        database.add_category(category)
    parent_dir = "static/images/Product_img"
    path = os.path.join(parent_dir, p_id)
    os.mkdir(path)
    UPLOAD_FOLDER = f'static/images/Product_img/{p_id}'
      # Any random secret key
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    if 'files[]' not in request.files:
        print('No file part')
    files = request.files.getlist('files[]')
    file_path = []
    for file in files:
        if file.filename == '':
            print('No image selected for uploading')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #print('upload_image filename: ' + filename)
            file_path.append(file.filename)
            print('Image successfully uploaded and displayed below')
        else:
            print('Allowed image types are - png, jpg, jpeg, gif')
    print(file_path)
    temp_name = ""
    for y in file_path:
        temp_name+="," + str(y)
    print(temp_name)
    img_path = temp_name
    qr_path = f"/static/images/Product_qr/{p_id}.png"
    data = f"{id}"
    qr = generate_qrcode.generate(data)
    qr.save(f"static/images/Product_qr/{p_id}.png")
    update_date = str(datetime.datetime.today())[:-16]
    database.add_product(p_id,p_name,p_rate,weight,w_unit,p_desc,category,Dimension,img_path,qr_path,placement,name,update_date,quantity,quan_unit,fragile,min_quan,10,s_rate)
    return redirect('/manage_products')

@app.route('/edit_product_details/<string:pid>', methods=["GET", "POST"])
def edit_product_details(pid):

    if not 'Admin' in session:
        return redirect('/admin_login')

    id = pid
    p_name = request.form['P_Name']
    p_rate = request.form['P_Rate']
    s_rate = request.form['S_Rate']
    weight = request.form['Weight']
    w_unit = request.form['w_unit']
    desc = request.form['P_desc']
    cate = request.form['cate']
    dimen = request.form['Dimension']
    placement = request.form['Placement_In_Warehouse']
    lower_bound = request.form['lower_bound']
    temp = database.getCategory()
    tempc = []
    for x in temp:
        tempc.append(x[0])
    if cate not in tempc:
        database.add_category(cate)
    data = f"{id}"
    qr = generate_qrcode.generate(data)
    qr.save(f"static/images/Product_qr/{id}.png")
    database.edit_product_details(id,p_name,p_rate,s_rate,weight,w_unit,desc,cate,dimen,placement,lower_bound ) 
    print("REACHED")

    return redirect('/manage_products')


@app.route('/manage_products')
def manage_employe():

    if not 'Admin' in session:
        return redirect('/admin_login')

    data = database.getMainProductData()
    return render_template('manage_products.html', NAME=session['Admin'], data=data)

@app.route('/delete_product/<string:pid>')
def delete_product(pid):
    if not 'Admin' in session:
        return redirect('/admin_login')

    print(pid)
    print(database.deleteProduct(pid))
    return redirect('/manage_products')

@app.route('/activate_product/<string:pid>')
def activate_product(pid):
    if not 'Admin' in session:
        return redirect('/admin_login')

    print(pid)
    print(database.activateProduct(pid))
    return redirect('/manage_products')

@app.route('/manage_suppliers')
def manage_suppliers():

    if not 'Admin' in session:
        return redirect('/admin_login')

    data = database.getAllSuppliers()
    return render_template('manage_supplier.html', NAME=session['Admin'], data=data)



@app.route('/add_new_supplier/<string:c_check>', methods=["GET", "POST"])
def add_new_supplier(c_check):
    if not 'Admin' in session:
        return redirect('/admin_login')

    msg = ""
    if c_check == 'false':
        msg = "Company already Existed"
    P_ids_list = request.form.getlist('select_product')
    P_ids = ""
    for P_id in P_ids_list:
        P_ids += P_id + ','
    return render_template('add_new_supplier.html', P_ids=P_ids, msg=msg)

@app.route('/select_products_supplier')
def select_products_supplier():
    if not 'Admin' in session:
        return redirect('/admin_login')
    data = database.getMainProductData(True)
    msg = ""
    if data == []:
        msg = "All Products are assigned to the Suppliers"
    return render_template('select_products_supplier.html', data=data, NAME=session['Admin'], msg=msg)

@app.route('/add_new_supplier_action', methods=["GET", "POST"])
def add_new_employee_action():

    name = request.form['fname']
    email = request.form['Email']
    phone = request.form['PhNumber']
    company_name = request.form['company_name']
    product_id = request.form['product_id']
    address = request.form['Address']
    company_exist = bool(database.checkCompany(company_name))
    if company_exist == False:
        return redirect('/add_new_supplier/false')
    sid = database.add_supplier(name, phone, address, email, company_name, product_id)
    database.addProductSupplier(product_id, sid)
    return redirect('/manage_suppliers')


@app.route('/remove_supplier/<string:sid>', methods=["GET", "POST"])
def remove_supplier(sid):

    if not 'Admin' in session:
        return redirect('/admin_login')

    database.removeSupplier(sid)
    return redirect('/manage_suppliers')



@app.route('/edit_employee/<string:id>', methods=["GET", "POST"])
def edit_employee(id):
    if not 'Admin' in session:
        return redirect('/admin_login')

    database.remove_user(id)
    return redirect('/Manage_Employees')


@app.route('/employee_details/<string:id>', methods=["GET", "POST"])
def employee_details(id):
    if not 'Admin' in session:
        return redirect('/admin_login')

    details = database.getEmployeeDetails(id)
    details = details[0]
    login_history = database.getEmployeeLoginHistory(id)
    return render_template('employee_details_manage_employee.html', x=details, history=login_history, NAME=session['Admin'])



# Admin Details 
@app.route('/your_details')
def your_details():
    data1 = database.getAdminDetails(session['Admin'])
    id_ = database.getAdminID(session['Admin'])
    id_ = id_[0][0]
    data2 = database.getAdminLoginHistory(id_)
    return render_template('admin_profile.html', NAME=session['Admin'], data1=data1, data2=data2)


@app.route('/edit_product_inventory_action/<string:pid>', methods=["GET", "POST"])
def edit_product_inventory_action(pid):
    quantity = request.form["quantity"]
    operation = request.form["operation"]
    database.editProductInventory(quantity, operation,pid)
    if not 'Admin' in session:
        return redirect('/admin_login')
    return redirect('/manage_products')


@app.route('/edit_product_inventory_action_employee/<string:pid>', methods=["GET", "POST"])
def edit_product_inventory_action_employee(pid):
    quantity = request.form["quantity"]
    operation = request.form["operation"]
    database.editProductInventory(quantity, operation,pid)
    if not 'Employee' in session:
        return redirect('/buyer_login')
    return redirect('/employee_manage_products')


@app.route('/edit_products/<string:id>', methods=["GET", "POST"])
def edit_products(id):
    if not 'Admin' in session:
        return redirect('/admin_login')

    data = database.getDetailedProductsData(id)
    category = database.getCategory()
    return render_template('edit_products.html',NAME = name, data = data, category = category)

@app.route('/manage_orders')
def manage_orders():
    data = []
    temp_data = database.getAllOrdersDetails()
    for x in temp_data:

        product_name = database.getProductName(x[2])[0][0]
        Buyer_name = database.getBuyerName('none', x[1])[0]

        temp = x
        temp = temp + (product_name, Buyer_name,)
        data.append(temp)
    return render_template('manage_orders.html', NAME=session['Admin'], data=data)

@app.route('/filter_manage_orders', methods=["GET", "POST"])
def filter_orders():
    filter = request.form['filter']
    if filter == 'all':
        return redirect('/manage_orders')
    oids = database.getFilteredOrders(filter)
    data = []
    for x in oids:
        temp = database.getOrderDetails(x)[0]
        data.append(temp)
    return render_template('manage_orders.html', NAME=session['Admin'], data=data)
#####################################################
#   Employee related Operations
#####################################################


"""
@app.route('/employee_login')
def employee_login():
    return render_template('employee_login.html')"""


@app.route('/employee_login_validation/<string:email>/<string:psw>', methods=["GET", "POST"])
def employee_login_validate(email, psw):
    post = 'Employee'
    is_valid = database.validate_login(email, psw, post)
    if is_valid:
        query = f"""
            select user_details_name from user_details where email = '{email}';
        """
        session['Employee_name'] = database.Database_common_operations.run_query_and_return_all_data(query)[0][0]
        session['Employee'] = email
        return redirect(f'/employee_panel')

    flash("email/password is incorrect!")
    return redirect('/buyer_login')

@app.route('/employee_logout')
def employee_logout():
    session.pop('Employee', None)
    return redirect('/')



#####################################################
#   Buyer related Operations
#####################################################



@app.route('/buyer_login')
def buyer_login():
    return render_template('buyer_login.html')


@app.route('/buyer_sign_up')
def sign_up_Buyer():
    return render_template('/buyer_sign_up.html')

@app.route('/add_buyer', methods=["GET", "POST"])
def add_buyer():
    email_c = request.form['Email']
    f_name = request.form['fname']
    ph_number = request.form['PhNumber']
    PSWT = request.form['pswt']
    PSW = request.form['psw']
    POST = 'Buyer'
    if PSWT == PSW:
        PASS = PSW
    else:
        print(PSW)
        print(PSWT)
        return redirect('/buyer_sign_up')
    opt_number = request.form['PhNumber2']
    Gender = request.form['Gender']
    B_date = request.form['DOB']
    print(B_date)
    Address = request.form['Address']
    State = request.form['countrya']
    City = request.form['district']
    """
email: str, user_name: str, ph_number, password: str, post: str, gender: str, birth: str, address: str,
 city: str, state: str,opt_number = 0
"""

    # check if the Buyer email is already in use..

    if not database.check_email_avail(email_c):
        flash("Email address is already in use!")
        return redirect('/buyer_sign_up')

    res = database.sign_up(email_c, f_name, ph_number, PASS, POST, Gender, B_date, Address, City, State, opt_number)
    return redirect('/')


@app.route('/buyer_login_validation', methods=["GET", "POST"])
def buyer_login_validate():
    email = request.form['email']
    password = request.form['psw']
    temp = database.getEmployee_emails()
    for x in temp:
        if email == x[0]:
            return redirect(f'/employee_login_validation/{email}/{password}')
    post = 'Buyer'
    is_valid = database.validate_login(email, password, post)
    if is_valid:
        query = f"""
            select email from user_details where email = '{email}'
        """
        name_b = database.Database_common_operations.run_query_and_return_all_data(query)[0][0]
        session['Buyer'] = name_b
        return redirect('/')
    flash("email/password is incorrect!")
    return redirect('/buyer_login')


@app.route('/buyer_logout')
def buyer_logout():
    session.pop('Buyer', None)
    return redirect('/')


@app.route('/manage_buyers')
def manage_buyers():
    if not 'Admin' in session:
        return redirect('/admin_login')

    data = database.getBuyerDetails()
    return  render_template('manage_buyers.html', NAME=session['Admin'], data=data)


@app.route('/order_status/<string:oid>', methods=["POST", "GET"])
def order_status(oid):
    status = request.form['status']
    database.setOrderStatus(oid, status)
    path = request.form['path']
    return redirect(path)


@app.route('/more_details_product/<string:pid>')
def more_details_products(pid):
    data = database.getDetailedProductsData(pid)
    img_path = database.getImgpath(pid)[0]
    print(img_path)
    name1 = ""
    try:
        name1 = session['Admin']
    except:
        name1 = session['Employee']
    return render_template('more_product_details.html', data=data, NAME=name1, img_pat=img_path)

@app.route('/employee_panel')
def employee_panel():
    
    NumberOfProducts_ = database.getNumberOfProducts()
    NumberOfOrders_ = database.getNumberOfPendingOrders()
    print(NumberOfOrders_)
    return render_template('try_employee_home.html', NAME=session['Employee_name'],
                           NumberOfProducts=NumberOfProducts_,
                           NumberOfOrder=NumberOfOrders_)

@app.route('/employee_manage_products')
def employee_manage_products():
    if 'Employee' not in session:
        return redirect('/buyer_login')

    data = database.getMainProductData()
    return render_template('employee_manage_products.html', NAME=session['Employee_name'], data=data)

@app.route('/employee_manage_orders')
def employee_manage_orders():
    if 'Employee' not in session:
        return redirect('/buyer_login')

    data = database.getAllOrdersDetails()
    return render_template('employee_manage_orders.html', NAME=session['Employee_name'], data=data)

@app.route('/buy_product/<string:pid>/<string:quantity>')
def buy_product(pid,quantity):
    if not 'Buyer' in session:
        return redirect('/buyer_login')
    items = 1
    data = database.getDetailedProductsData(pid)
    img = database.getImgpath(pid)[0]
    pro_price = int(data[0][18])*int(quantity)
    total_price = int(data[0][18])*int(quantity)+70
    return render_template('shopping_cart.html',pro_price=pro_price ,QUAN=items, data=data, img_path=img, quantity=quantity, total_price=total_price)

@app.route('/inc_quantity/<string:pid>/<string:quantity>')
def inc_quantity(pid,quantity):
    p_quantity = int(database.getDetailedProductsData(pid)[0][13])
    temp = int(quantity)
    if temp >= p_quantity:
        flash('stock not available')
        return redirect(f'/buy_product/{pid}/{temp}')
    temp += 1
    return redirect(f'/buy_product/{pid}/{temp}')

@app.route('/dec_quantity/<string:pid>/<string:quantity>')
def dec_quantity(pid,quantity):
    temp = int(quantity)
    if temp <= 0:
        return redirect(f'/buy_product/{pid}/0')
    temp -= 1
    return redirect(f'/buy_product/{pid}/{temp}')


@app.route('/multiple_shopping_cart/<string:pid>/<string:quantity>')
def shopping_cart(pid,quantity):
    if not 'Buyer' in session:
        return redirect('/buyer_login')
    validProduct = database.validateCartProduct(session['Buyer'],pid)
    if validProduct:
        return redirect('/show_multiple_shopping_cart')
    res = database.addProductInCart(session['Buyer'], pid, quantity)
    print(res)
    items = database.getNoOfItemsInCart(session['Buyer'])
    data = []
    Total_price = 0
    info_products = database.getProductsFromCart(session['Buyer'])
    Products = {}
    for y in info_products:
        Products[y[0]] = y[1]
    print(Products)
    for x in Products:
        print(x)
        temp = database.getDetailedProductsData(x)[0]
        temp_img = database.getImgpath(x)[0]
        temp = temp + (temp_img,)
        p_quantity = int(database.getDetailedProductsData(x)[0][13])
        msg = " "
        if int(Products[x]) > p_quantity:
            msg = "stock not available"
        pro_quan = Products.get(x)
        sum_price = int(Products[x]) * int(temp[18])
        temp = temp + (pro_quan, msg, sum_price,)
        Total_price += int(Products[x])*int(temp[18])
        data.append(temp)
    return render_template('multiple_shopping_cart.html', data=data, QUAN=items, total_price=Total_price)

@app.route('/show_multiple_shopping_cart')
def show_shopping_cart():
    if not 'Buyer' in session:
        return redirect('/buyer_login')
    items = database.getNoOfItemsInCart(session['Buyer'])
    data = []
    Total_price = 0
    info_products = database.getProductsFromCart(session['Buyer'])
    products = {}
    for y in info_products:
        products[y[0]] = y[1]
    for x in products:
        print(x)
        temp = database.getDetailedProductsData(x)[0]
        temp_img = database.getImgpath(x)[0]
        temp = temp + (temp_img,)
        p_quantity = int(database.getDetailedProductsData(x)[0][13])
        msg = " "
        print(f"Product:{products[x]}")
        print(f"quantity: {p_quantity}")
        if int(products[x]) >= p_quantity:
            msg = "stock not available"
        pro_quan = products.get(x)
        sum_price = int(products[x]) * int(temp[18])
        temp = temp + (pro_quan, msg, sum_price,)
        Total_price += int(products[x]) * int(temp[18])
        data.append(temp)
        session['user_cart_total'] = Total_price

    return render_template('multiple_shopping_cart.html', data=data, QUAN=items, total_price=Total_price)


@app.route('/mul_inc_quantity/<string:pid>')
def mul_inc_quantity(pid):
    database.incQuantityInCart(session['Buyer'], pid)
    return redirect('/show_multiple_shopping_cart')


@app.route('/mul_dec_quantity/<string:pid>')
def mul_dec_quantity(pid):
    query = f"""
        select product_quantity from shopping_cart where(buyer_email = '{session['Buyer']}' AND product = '{pid}');
    """
    temp = int(database.Database_common_operations.run_query_and_return_all_data(query)[0][0])
    if temp <= 0:
        return redirect('/show_multiple_shopping_cart')
    database.decQuantityInCart(session['Buyer'], pid)
    return redirect('/show_multiple_shopping_cart')


@app.route('/cancel_product/<string:pid>')
def cancel_product(pid):
    res = database.deleteProductFromCart(session['Buyer'], pid)
    print(res)
    return redirect('/show_multiple_shopping_cart')


@app.route('/all_products', methods=["GET", "POST"])
def all_products():
    if 'Buyer' not in session:
        login = "false"
    else:
        login = "true"
    try:
        print("Reach1")
        f_category = request.form['category']
        print("Reach2")
        f_price = int(request.form['price'])
        print("Reach3")
        if f_price <= 0:
            f_price = int(database.getMinAndMaxProPrice()[1])
        f_quantity = int(request.form['quantity'])
        print("Reach4")
        f_company = request.form['company']
        print("Reach5")
        data = database.getFilteredProducts(f_category, f_price, f_quantity, f_company)
        print("Reach6")
    except Exception as err:
        print(err)
        print(type(err).__name__)
        data = database.getProductsforDisplay()
    product_names = database.getProductsforDisplay()
    data_list = []
    for a in product_names:
        data_list.append(a[1])
    categories_data = database.getCategory()
    categories = []
    company = database.getCompanies()
    for b in categories_data:
        categories.append(b[0])
    min = int(database.getMinAndMaxProPrice()[0])
    max = int(database.getMinAndMaxProPrice()[1])
    try:
        return render_template('all_products.html', data=data, login=login, data_list=data_list, categories=categories,
                               min_p=min, max_p=max, company=company, f_company=f_company, f_category=f_category,
                               f_price=f_price, f_quantity=f_quantity)
    except:
        return render_template('all_products.html', data=data, login=login, data_list=data_list, categories=categories,
                               min_p=min, max_p=max, company=company, f_company='All', f_category='All',
                               f_price=0, f_quantity=0)

@app.route('/buyer_details/<string:id>')
def buyer_details(id):
    data = database.getBuyerDetails(id)
    order_data_temp = database.getOrderDetails(id)
    order_data = []
    for x in order_data_temp:
        final = x
        name = database.getDetailedProductsData(x[2])[0][1]
        final += (name,)
        order_data.append(final)
    reviews = database.getReviews(id)
    return render_template('Buyer_Details.html', data=data, NAME=session['Admin'], order_data=order_data, reviews=reviews)

@app.route('/cancel_order/<string:oid>')
def cancel_order(oid):
    database.cancelOrder(oid)
    return redirect('/manage_orders')

@app.route('/searched_products', methods=["POST", "GET"])
def searched_products():
    if 'Buyer' not in session:
        login = "false"
    else:
        login = "true"
    product = request.form['search']
    product = product.lower()
    product_names = database.getProductsforDisplay()
    temp = {}
    for x in product_names:
        name = str(x[1]).lower()
        temp[x[0]] = name
    matched = []
    for y in temp.values():
        if product in y:
            id = database.get_key(y, temp)
            matched.append(id)
    data = []
    for z in matched:
        te = database.getProductsforDisplay(0,z)[0]
        data.append(te)
    data_list = []
    for a in product_names:
        data_list.append(a[1])
    return render_template('all_products.html', data=data, login=login, data_list=data_list)

@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    if 'Buyer' not in session:
        return redirect('/buyer_login')
    fname = request.form['fname']
    lname = request.form['lname']
    email = session['Buyer']
    subject = request.form['subject']
    message = request.form['message']
    print(database.addFeedback(fname, lname, email, subject, message))
    path = request.form['path']
    print("Feedback submitted")
    return redirect(path)

@app.route('/checkout')
def checkout():
    if 'Buyer' not in session:
        return redirect('/buye_login')

    # Current shipping addrress of the customer..

    addr = database.get_current_shipping_address(session['Buyer'])
    print(addr)
    return render_template('confirm_address.html', shipping_addr=addr)


@app.route('/confirm_address', methods=["GET", "POST"])
def confirm_address():

    addr = request.form['addr']
    addr_ = database.get_current_shipping_address(session['Buyer'])
    if addr != addr_:
        session['Buyer_new_shipping'] = addr
    
    return render_template('credit_card_checkout.html', total_payable=session['user_cart_total'], email=session['Buyer'])
     


@app.route('/validate_credit_card_details', methods=["GET", "POST"])
def validate_credit_card_details():
    if 'Buyer' not in session:
        return redirect('/buye_login')

    nameOnCard  = request.form['name']
    cardNumber = request.form['card-num']
    cardExp = request.form['exp']
    cardCvv = request.form['cvv']
    cardNumber = cardNumber.replace(" ", "")

    if not validateCard.validateCard(str(cardNumber)):
        flash("PLease enter valid credit card details!")
        return render_template('credit_card_checkout.html', total_payable=session['user_cart_total'],email=session['Buyer'])
    
    status = makePayment.makePayment(cardNumber, cardCvv, nameOnCard, cardExp, session['user_cart_total'])
    if not status:
        flash("Payment Failed please try again!")
        return render_template('credit_card_checkout.html', total_payable=session['user_cart_total'],email=session['Buyer'])

    
    shipping_addr = ""

    if 'Buyer_new_shipping' in session:
        shipping_addr = session['Buyer_new_shipping']
        session.pop('Buyer_new_shipping', None)
    
    else:
        shipping_addr = database.get_current_shipping_address(session['Buyer'])


    payment_status = "true"
    payment_method = "card"
    amount, bill_number, product_images, quantity, product_price, product_name = generateBill.generateBill(session['Buyer'], shipping_addr, payment_status)
    username = database.getBuyerName(session['Buyer'])
    order_date = datetime.date.today()

    # data list for html page 
    try:
        new_addr = shipping_addr.split('\n')
        new_addr = new_addr[0] + ", " + new_addr[1] + ", " + new_addr[2] + "." 
    except:
        new_addr = shipping_addr
    data = []
    print(product_images, product_name, product_price, quantity)
    for i in range(len(product_name)):
        temp = (product_name[i], product_price[i], product_images[i], quantity[i])
        print(temp)
        data.append(temp)
       
    
    print(data)

    # Generate bills
    print(product_name[0], product_price, quantity)
    generateBillPdf.generateBill(bill_number, product_name[0], product_price, quantity, amount )

    return render_template('order_confirmed.html', date_=order_date, data=data, 
    payment_method=payment_method, bill_number=bill_number, buyer_name=username, shipping_addr=new_addr,
    total=amount)


@app.route('/download_invoice/<string:bill_id>')
def send_invoice(bill_id):
    
    return send_file(f'Bills/{bill_id}.xlsx', attachment_filename="Invoice.xlsx")


# Need to be changed 
@app.route('/checkout_cod')
def checkout_cod():
    if 'Buyer' not in session:
        return redirect('/buyer_login')

    # Current shipping addrress of the customer..

    addr = database.get_current_shipping_address(session['Buyer'])
    print(addr)
     # Generate Bill return invoice
    payment_status = "flase" #pending 
    shipping_addr = addr

    payment_status = "false"
    payment_method = "COD"
    amount, bill_number, product_images, quantity, product_price, product_name = generateBill.generateBill(session['Buyer'], shipping_addr, payment_status)
    username = database.getBuyerName(session['Buyer'])
    order_date = datetime.date.today()

    # data list for html page 
    new_addr = shipping_addr.split('\n')
    new_addr = new_addr[0] + ", " + new_addr[1] + ", " + new_addr[2] + "." 
    data = []
    print(product_images, product_name, product_price, quantity)
    for i in range(len(product_name)):
        temp = (product_name[i], product_price[i], product_images[i], quantity[i])
        print(temp)
        data.append(temp)
       
    
    print(data)

    # Generate bills
    print(product_name[0], product_price, quantity)
    generateBillPdf.generateBill(bill_number, product_name[0], product_price, quantity, amount )

    return render_template('order_confirmed.html', date_=order_date, data=data, 
    payment_method=payment_method, bill_number=bill_number, buyer_name=username, shipping_addr=new_addr,
    total=amount)


@app.route('/your_orders')
def your_orders():
    if 'Buyer' not in session:
        return redirect('/buyer_login')
    
    details = database.getOrderHistory(session['Buyer'])  

    #Display records in decs order .. 
    details_rev = []
    for i in reversed(range(len(details))):
        details_rev.append(details[i])
    
    return render_template('your_orders.html', data=details_rev)


@app.route('/track_order/<string:order_id>', methods=["GET", "POST"])
def track_order(order_id):

    # value 1 - active step0
    # value 2 - step0

    status, date_ = database.getOrderStatus(order_id)
    status_ = ["Accepted", "ReadyToShip", "Shipped", "Delivered"]
    s = []
    date_ = date_.split('-')

    if status == status_[0]:
        s.append("active step0")
        s.append("step0")
        s.append("step0")
        s.append("step0")
        date_ = datetime.datetime(int(date_[0]), int(date_[1]), int(date_[2]))
        date_ += timedelta(days=7)

    if status == status_[1]:
        s.append("active step0")
        s.append("active step0")
        s.append("step0")
        s.append("step0")
        date_ = datetime.datetime(int(date_[0]), int(date_[1]), int(date_[2]))
        date_ += timedelta(days=6)
    
    if status == status_[2]:
        s.append("active step0")
        s.append("active step0")
        s.append("active step0")
        s.append("step0")
        date_ = datetime.datetime(int(date_[0]), int(date_[1]), int(date_[2]))
        date_ += timedelta(days=4)

    if status == status_[3]:
        s.append("active step0")
        s.append("active step0")
        s.append("active step0")
        s.append("active step0") 
        date_ = date_[0] + "-" + date_[1] + "-" + date_[2]

    return render_template('show_order_status.html', exp_date=date_, s=s)
   
product_ids = []
quantity = []
pnames = []

@app.route('/employee_add_bill',  methods=["GET", "POST"])
def employee_add_bill():


    try: 
        temp1 = request.form['product']
        #product_ids.append(temp1[0])

        temp1 = temp1.split(',')[0]
        temp1 = temp1[2:-1]
        product_ids.append(temp1)

        temp2 = request.form['product']
        temp2 = temp2.split(',')[1]
        temp2 = temp2[2:-1]
        pnames.append(temp2)

        quantity.append(str(request.form['quan']))
    except:
        pass 

    

    data = database.getProductDataForEmployee()
    data1 = []
    for x in range(len(product_ids)):
        data1.append((pnames[x], quantity[x], ))


    return render_template('employee_add_bill.html', NAME=session['Employee_name'], data=data, data1=data1)




@app.route('/register_offline_customer',  methods=["GET", "POST"])
def register_offline_customer():

    exist = request.form['cExist']
    email = request.form['cEmail']
    name = request.form['cName']
    number = request.form['cNumber']
    opt_number = request.form['cNumber_opt']
    gender = request.form['cGen']
    bdate = request.form['bDate']
    address = request.form['addr']
    state = request.form['countrya']
    city = request.form['district']

    return "Generated"
    


@app.route('/get_bill_data_employee',  methods=["GET", "POST"])
def get_bill_data_employee():
    return "working"



@app.route('/checkout_cod_one')
def checkout_cod_one():
    pass


@app.route('/checkout_one')
def checkout_one():
    if 'Buyer' not in session:
        return redirect('/buye_login')

    # Current shipping addrress of the customer..

    addr = database.get_current_shipping_address(session['Buyer'])
    print(addr)
    return render_template('confirm_address.html', shipping_addr=addr)


@app.route('/qrcode/<string:pid>')
def qrcode(pid):
    data = database.getDetailedProductsData(pid)
    img_path = database.getImgpath(pid)[0]
    return render_template('qr_product_details.html', data=data, img_pat=img_path)


@app.route('/add_supplier_product/<string:sid>')
def add_supplier_product(sid):
    if not 'Admin' in session:
        return redirect('/admin_login')

    data = database.getMainProductData(True)
    Sup_data = database.getSupplierProducts(sid)
    for s in Sup_data:
        data.append(s)
    msg = ""
    if data == []:
        msg = "All Products are assigned to the Suppliers"
    return render_template('add_supplier_product.html', data=data, NAME=session['Admin'], msg=msg, sid=sid)

@app.route('/add_supplier_product_action/<string:sid>', methods=["GET", "POST"])
def add_supplier_product_action(sid):
    P_ids_list = request.form.getlist('select_product')
    P_ids = ""
    for P_id in P_ids_list:
        P_ids += P_id + ','
    database.updateSupplierProducts(sid,P_ids)
    return redirect('/manage_suppliers')
    

if __name__ == "__main__":
    app.run(host="localhost", port=5050, debug=True)  # host="0.0.0.0", port=5000