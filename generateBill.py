import database
import datetime 

def generateBill(email, shipping_addr, payment_status):
     
    # Payment done -- Generate bill and return invoice ..
    

    id_ = database.Database_common_operations.run_query_and_return_all_data(f"select id from user_details where email='{email}'")[0][0]
    print(id_)

    items = database.getProductsFromCart(email)
    print(items)
    quantity_unit = "pcs"
    completed_ = "Accpeted"

    product_ids = []
    quantity = []
    order_ids = []

    date_ = datetime.date.today()

    for item in items:
        product_ids.append(item[0])
        quantity.append(item[1])
    

    # Generate Orders 
   

    for i in range(len(product_ids)):
        
        order_id = database.add_order(id_, product_ids[i], quantity[i], quantity_unit, completed_, date_)
        order_ids.append(order_id)


    print(order_ids)

    amount, number = database.add_bill(order_ids, shipping_addr, payment_status)
    
    # order wise get product image

    product_images = []
    for id in product_ids:
        print(id)
        product_images.append(database.getImgpath(id)[0]) # Only the first image 
    
    product_price = []
    product_name = []

    for i in product_ids:
        product_price.append(database.getProductSellingPrice(i))
        product_name.append(database.getProductName(i))

    

    

    for i in product_ids:
        database.deleteProductFromCart(email, i)

    return amount, number, product_images, quantity, product_price, product_name

#generateBill('azim_baldiwala@gmail.com', "testing")