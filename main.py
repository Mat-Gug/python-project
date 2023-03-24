from product import Product
from utils import *
from time import sleep


if __name__=="__main__":

    cmd = None

    while cmd!="close":
        
        cmd = input("Enter a command: ")
        
        if cmd=="add":
            
            add_product_in_warehouse("warehouse.tsv")
            
        elif cmd=="list":
            
            make_list("warehouse.tsv")
                
        elif cmd=="sale":
            
            sell_product("warehouse.tsv", "sales_file.tsv")
        
        elif cmd=="profits":
        
            get_profit("sales_file.tsv")
            
        elif cmd=="help":
            
            help_message()
        
        elif cmd=="close":
            
            print("Bye bye")
            sleep(1)
        
        else:
            
            print("Invalid command")
            help_message()
