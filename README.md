![warehouse_image](https://github.com/Mat-Gug/python_project/blob/master/warehouse.png)

# Python project: Warehouse Management Software 

Hello, thank you for being here! :smiley:

This project consists in realizing a software for the management of a market warehouse. The software has the following features:

- register new products, with name, quantity, sale price and purchase price;
- list all the available products;
- record the sales made;
- show the gross and net profits;
- show a help menu with all the available commands.

The available commands are:

- **add**: adds a product to the warehouse;
- **list**: lists the products in the warehouse;
- **sale**: records a sale made;
- **profits**: shows the gross and net profits;
- **help**: shows the available commands;  
- **close**: quits the program. 

The program creates two files, `warehouse.tsv` and `sales_file.tsv`, which keep track of the products in the warehouse and the sales, respectively.<br> Furthermore, it properly validates the user input: for example, it checks that the quantity is an integer number and performs a case-insensitive comparison between the names of the products in the warehouse and the ones entered by the user.
