import shutil 
from csv import DictReader, DictWriter
from tempfile import NamedTemporaryFile 


class Product:
    
    """
    This class represents a product.
    """
    
    def __init__(self, d):
        
        """
        d (list) : dictionary with the following keys:
                   - "PRODUCT"
                   - "QUANTITY"
                   - "PURCHASE PRICE"
                   - "PRICE"
        """

        self._d = {}
        
        for key in d.keys():
            if key=="PRODUCT":
                self._d[key] = d[key]
            elif key=="QUANTITY":
                self._d[key] = int(d[key])
            else:
                self._d[key] = float(d[key])
    
    def __getitem__(self, key):

        """
        This function returns the value associated to a given key.

        Positional arguments:
        key : str -- key of which we want to know the value
        """

        return self._d[key]
    
    def __setitem__(self, key, new_value):

        """
        This function assigns a new value to a given key.

        Positional arguments:
        key : str -- key of which we want to change the value
        """

        self._d[key] = new_value
    
    def add(self, file_name):

        """
        Addition of a product to the warehouse.
    
        Positional arguments:
        file_name : tsv file -- file containing the products in the warehouse
        """
        
        with open(file_name, "a+", encoding = "utf-8", newline="") as f:        
            if f.tell() == 0:
                columns = ["PRODUCT", "QUANTITY", "PURCHASE PRICE", "PRICE"]
                f_writer = DictWriter(f, fieldnames=columns, delimiter = "\t")
                f_writer.writeheader()
                f_reader = DictReader(f, delimiter = "\t")
            else:
                f.seek(0)
                f_reader = DictReader(f, delimiter = "\t")
                columns = f_reader.fieldnames
                f_writer = DictWriter(f, fieldnames=columns, delimiter = "\t")
                f.seek(0, 2)

            f_writer.writerow(self._d)
    
    def update(self, file_name, subtract = False):

        """
        Update of a product to the warehouse.
    
        Positional arguments:
        file_name : tsv file -- file containing the products in the warehouse
    
        Keyword arguments:
        subtract : bool (default False) -- if True, it makes the difference between the quantity of the product in the file
                                           and that of the object Product, otherwise it returns the sum of the two values.   
        """
    
        tempfile = NamedTemporaryFile(mode='w', delete=False, encoding="utf-8", newline="")

        with open(file_name, encoding = "utf-8", newline="") as f, tempfile:
            f_reader = DictReader(f, delimiter="\t")
            fieldnames = f_reader.fieldnames
            f_writer = DictWriter(tempfile, fieldnames=fieldnames, delimiter="\t")
            f_writer.writeheader()
            for row in f_reader:
                if row["PRODUCT"] == self._d["PRODUCT"]:
                    if subtract and int(row["QUANTITY"])>self._d["QUANTITY"]:        
                        row["QUANTITY"] = int(row["QUANTITY"]) - self._d["QUANTITY"]        
                    elif not subtract:                    
                        row["QUANTITY"] = int(row["QUANTITY"]) + self._d["QUANTITY"]                        
                    else:                        
                        continue
                f_writer.writerow(row)

        shutil.move(tempfile.name, file_name)
