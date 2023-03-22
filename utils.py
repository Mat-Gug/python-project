import shutil 
from csv import DictReader, DictWriter
from tempfile import NamedTemporaryFile

from product import Product


def is_integer_and_positive(n):
    
    """
    This function checks if a given string represents a positive integer number. 

    Positional arguments:
    n : str
    """
    
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer() and float(n)>0

    
def is_float_and_positive(n):
    
    """
    This function checks if a given string represents a positive float number. 

    Positional arguments:
    n : str 
    """
    
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True and float(n)>=0
    
    
def validate_string(question, function):

    """
    This function validates the input answer to a given question according to a function we choose.
    
    Positional arguments:
    question : str -- question to answer
    function : function -- function that validates the string
    """
    
    n = input(question)
    
    while not function(n):
        print("Invalid value.")
        n = input(question)
    
    return n
    

def is_present(product_name, file_name, name_column = "PRODUCT"):
    
    """
    This function checks if a given product is present in the warehouse.
    
    Positional arguments:
    product_name : str -- name of the product
    file_name : tsv file -- file containing the products in the warehouse
    
    Keyword arguments:
    name_column : str (default "PRODUCT") -- name of the column with the names of the products
    """
    
    if is_empty(file_name):
        return False
    
    with open(file_name, encoding = "utf-8") as f:
        f_reader = DictReader(f, delimiter="\t")
        is_present = False
            
        for row in f_reader:
            if row[name_column]==product_name.lower():
                is_present = True
            
    return is_present


def validate_answer(question):

    """
    This function validates the input answer to a given question and returns it only when is "yes" or "no".
    
    Positional arguments:
    question : str -- question to answer
    """
    
    answer = input(question)
    
    while answer not in ("yes", "no"):
        print("Invalid answer.")
        answer = input(question)
        
    return answer


def get_remaining_product_properties_from_warehouse(partial_product, file_name):
    
    """
    This function returns the Product object associated to a given product of which we only have partial information.
    
    Positional arguments:
    partial_product : dict -- dictionary with some of the properties of the product. The only requirement is the presence of the item with key "PRODUCT"
    file_name : tsv file -- file from which the remaining properties of the product are obtained
    """
    
    with open(file_name, encoding = "utf-8", newline="") as f:
        f_reader = DictReader(f, delimiter="\t")
        product = partial_product

        for row in f_reader:
            try:
                if row["PRODUCT"] == partial_product["PRODOTTO"]:
                    for key in set(row.keys())-set(partial_product.keys()):
                        product[key] = row[key]
            except KeyError:
                print("The key 'PRODUCT' is not present in the dictionary.")

    return Product(product)


def is_empty(warehouse_file_name):
    
    """
    This function checks if there are products in the warehouse.
    
    warehouse_file_name : tsv file -- file containing the products in the warehouse
    """
    
    try:
        total_product_rows = sum(1 for _ in open(warehouse_file_name, encoding = "utf-8", newline=""))-1
    except FileNotFoundError:
        return True 
    else:
        if total_product_rows == 0:
            return True
        return False

    
def print_sold_products(products):
    
    """
    This function prints the products sold during a given transaction.
    
    products : dict -- dictionary where the keys are the product names, while the values are given by lists, where:
                       -index 0: quantity of the product
                       -index 1: price of the product
    """
    
    if len(products)!=0:
        OUTPUT="SALE REGISTERED\n\n"
        for key in products.keys():
            OUTPUT+="\u2022 {quantity} X {name} : \u20ac{price}\n".format(quantity = products[key][0],
                                                                      name = key, 
                                                                      price = products[key][1])

        print(OUTPUT)


def add_product_in_warehouse(file_name):
    
    """
    This function adds a product in the warehouse.
    
    Positional arguments:
    file_name : tsv file -- file containing the products in the warehouse
    """
    
    product_name = input("Name of the product: ")
    product_quantity = validate_string("Quantity: ", is_integer_and_positive)

    if is_present(product_name, file_name):
        product = get_remaining_product_properties_from_warehouse({"PRODUCT": product_name.lower(), "QUANTITY" : product_quantity}, file_name)
        product.update(file_name)
    else:
        product_purchase_price = validate_string("Purchase price: ", is_float_and_positive)
        product_sale_price = validate_string("Sale price: ", is_float_and_positive)
        
        product = Product({"PRODUCT": product_name.lower(), 
                           "QUANTITY" : product_quantity, 
                           "PURCHASE PRICE" : product_purchase_price, 
                           "PRICE" : product_sale_price})
        product.add(file_name)

    print(f"ADDED: {product['QUANTITY']} X {product['PRODUCT']}")

        
def sell_product(warehouse_file_name, sales_file_name):
    
    """
    This function sells a product from the warehouse and adds it to the file with the sold products.
    
    Positional arguments:
    file_name : tsv file -- file containing the products in the warehouse
    sales_file_name : tsv file -- file containing the sold products
    """
    
    if is_empty(warehouse_file_name):
        print("There are no products in the warehouse.")
        return
            
    with open(warehouse_file_name, "a+", encoding = "utf-8", newline = "") as f:
        f_reader = DictReader(f, delimiter="\t")
        columns = f_reader.fieldnames
        answer = None
        sold_products = {}

        while answer!="no":
            still_continue = None
            still_want = None
            still_buy = None            
            product_name = input("Name of the product: ")
            while not is_present(product_name, warehouse_file_name) and still_continue!="no":
                print("This product is not present in the warehouse.")
                still_continue = validate_answer("Do you want to continue with your purchase? (yes/no): ")
                if still_continue =="yes":
                    product_name = input("Name of the product: ")
            if still_continue =="no":
                break

            product = get_remaining_product_properties_from_warehouse({"PRODUCT": product_name.lower()}, warehouse_file_name)
            product_quantity = int(validate_string("Quantity: ", is_integer_and_positive))

            while int(product['QUANTITY'])<product_quantity and still_want!="no":
                print(f"The available quantity of the product '{product_name}' is {product['QUANTITY']}.")
                still_want = validate_answer("Do you still want to purchase this product? (yes/no): ")
                if still_want=="yes":
                    product_quantity = int(validate_string("Quantity: ", is_integer_and_positive))
                else:
                    still_buy = validate_answer("Do you want to buy other products? (yes/no): ")
            
            if still_buy == "yes":
                still_buy = None 
                continue
            elif still_buy == "no":
                break

            product["QUANTITY"] = product_quantity
            
            if is_present(product_name, sales_file_name):
                product.update(sales_file_name)
            else: 
                product.add(sales_file_name)

            product.update(warehouse_file_name, subtract=True)

            if product["PRODUCT"] in sold_products.keys(): 
                sold_products[product["PRODUCT"]][0] += product["QUANTITY"]
            else:
                sold_products[product["PRODUCT"]] = [product["QUANTITY"], product["PRICE"]]

            answer = validate_answer("Do you want to add another product? (yes/no): ")

        print_sold_products(sold_products)
    
    
def get_profit(sales_file_name):
    
    """
    This function computes and prints the gross and net profit.
    
    Positional arguments:
    sales_file_name : tsv file -- file containing the sold products
    """
    
    if is_empty(sales_file_name):
        print("No product has been sold yet.")
        return

    with open(sales_file_name, encoding = "utf-8", newline="") as f:
        f_reader = DictReader(f, delimiter="\t")
        fieldnames = f_reader.fieldnames
        gross_profit = 0
        total_purchase_cost = 0

        for row in f_reader:
            gross_profit += float(row["PRICE"])*int(row["QUANTITY"])
            total_purchase_cost += float(row["PURCHASE PRICE"])*int(row["QUANTITY"])

    print("Profit: gross=\u20ac%.2f net=\u20ac%.2f" % (gross_profit, gross_profit-total_purchase_cost))

    
def make_list(file_name, name_index = 0, quantity_index = 1, sale_price_index = 3):

    """
    This function prints the list of the products present in the warehouse.

    Positional arguments:
    file_name : tsv file -- file containing the products in the warehouse

    Keyword arguments:
    name_index : int (default 0) -- index of the column with the names of the products
    quantity_index : int (default 1) -- index of the column with the quantity of the products
    sale_price_index : int (default 3) -- index of the column with the sale prices of the products                                     
    """
    
    if is_empty(file_name):
        print("There are no products in the warehouse.")
        return
    
    with open(file_name, encoding = "utf-8") as f:            
            f_reader = DictReader(f, delimiter="\t")
            columns = f_reader.fieldnames
            print("%s\t%s\t%s" % (columns[name_index], columns[quantity_index], columns[sale_price_index]))
            
            for row in f_reader:                 
                print("%s\t%s\t\u20ac%s" % (row[columns[name_index]], row[columns[quantity_index]], row[columns[sale_price_index]]))
                

def help_message():

    """
    This function prints the help menu with all commands available.
    """
    
    print("The available commands are the following:\n\n"
          +"\u2022 add: adds a product to the warehouse\n"
          +"\u2022 list: lists the products in the warehouse\n"
          +"\u2022 sale: records a sale made\n"
          +"\u2022 profits: shows the total profits\n"
          +"\u2022 help: shows the available commands\n"
          +"\u2022 close: quit the program")
