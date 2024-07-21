import mysql.connector
from datetime import datetime
from tabulate import tabulate

mydb = mysql.connector.connect(
    host="localhost",
    user="amir",
    password="Amir@2003",
    database='starstore'
)
cursor = mydb.cursor()


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def change_password(self, new_password):
        self.password = new_password
        sql = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(sql,
                       (new_password, self.username))

        mydb.commit()
        print('Password changed successfully')

    @staticmethod
    def check_username(username, access):
        users = []
        if access == 1:
            users = Admin.all_admins
        elif access == 2:
            users = Customer.all_customers

        for user in users:
            if user[1] == username:
                return True
        return False

    @staticmethod
    def check_user(username, password, access):
        users = []
        if access == 1:
            users = Admin.all_admins
        elif access == 2:
            users = Customer.all_customers

        for user in users:
            if user[1] == username and user[2] == password:
                return True
        return False


class Admin(User):
    all_admins = []

    def __init__(self, username, password):
        super().__init__(username, password)

    def admin_panel(self):
        while True:
            print("\nAdmin Panel:")
            print("1. Add new product")
            print("2. Update product stock")
            print("3. Update product price")
            print("4. Change password")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == '1':
                self.add_new_product()
            elif choice == '2':
                self.update_product_stock()
            elif choice == '3':
                self.update_product_price()
            elif choice == '4':
                self.change_password_admin()
            elif choice == '5':
                admin_login()
            else:
                print("Invalid choice")

    def add_new_product(self):
        name = input('Enter product name (required): ')
        if len(name) == 0:
            print('Name is required')
            self.add_new_product()
        description = input('Enter product description: ')
        price = input('Enter product price (required): ')
        try:
            price = float(price)
        except:
            print('Enter valid number')
            self.add_new_product()
        category = input('Enter product category: ')
        stock = input('Enter product stock (required): ')
        try:
            stock = int(stock)
        except:
            print('Enter valid number')
            self.add_new_product()
        barcode = input('Enter product barcode (required): ')
        if len(barcode) == 0:
            print('Barcode is required')
            self.add_new_product()
        if Product.product_exists(barcode):
            print("Product with this barcode already exists.")
            return

        sql = """
        INSERT INTO products (name, description, price, category, stock, barcodeNumber)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (name, description, price, category, stock, barcode))
        mydb.commit()
        print("Product added successfully")
        self.admin_panel()

    def update_product_stock(self):
        barcode = input('Enter product barcode: ')
        if not Product.product_exists(barcode):
            print("Product with this barcode does not exist.")
            return
        print(f"Current stock: {Product.get_product_field_by_barcode(barcode, 'stock')}")
        new_stock = int(input('Enter new stock amount: '))
        Product.update_product_stock(barcode, new_stock)
        print("Product stock updated successfully")

    def update_product_price(self):
        barcode = input('Enter product barcode: ')
        if not Product.product_exists(barcode):
            print("Product with this barcode does not exist.")
            return
        print(f"Current price: {Product.get_product_field_by_barcode(barcode, 'price')}")
        new_price = float(input('Enter new price: '))
        Product.update_product('price', barcode, new_price)
        print("Product price updated successfully")

    def change_password_admin(self):
        current_password = input('Enter current password: ')
        if current_password != self.password:
            print('Incorrect password')
            return
        new_password = input('Enter new password: ')
        if not validate_password(new_password):
            print("Password must be at least 8 characters long, include an uppercase letter, and a number.")
            return
        self.change_password(new_password)

    @staticmethod
    def get_all_admins():
        query = "SELECT * FROM users WHERE access = 1"
        cursor.execute(query)
        Admin.all_admins = cursor.fetchall()


class Customer(User):
    all_customers = []

    def __init__(self, username, password):
        super().__init__(username, password)
        self.wallet_amount = 0
        self.load_wallet()

    def load_wallet(self):
        sql = "SELECT walletAmount FROM extrainfos WHERE personID = (SELECT personID FROM users WHERE username = %s)"
        cursor.execute(sql, (self.username,))
        result = cursor.fetchone()
        if result:
            self.wallet_amount = result[0]

    def customer_panel(self):
        while True:
            print(f"\nWelcome {self.username}, your wallet balance is: {self.wallet_amount}")
            print("1. Place a new order")
            print("2. View order history")
            print("3. Change password")
            print("4. Charge wallet")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == '1':
                self.place_order()
            elif choice == '2':
                self.view_order_history()
            elif choice == '3':
                self.change_password_customer()
            elif choice == '4':
                self.charge_wallet()
            elif choice == '5':
                customer_login()
            else:
                print("Invalid choice")

    def place_order(self):
        Product.display_all_products()
        order = []
        while True:
            entry = input("Enter 'barcode quantity' to add to order or 'done' to finish: ")
            if entry.lower() == 'done':
                break
            try:
                barcode, quantity = entry.split()
                quantity = int(quantity)
                product = Product.get_product_by_barcode(barcode)
                if product:
                    if quantity > product.stock:
                        print(f"Only {product.stock} units available")
                    else:
                        order.append((product, quantity))
                else:
                    print("Invalid barcode")
            except ValueError:
                print("Invalid input format. Use 'barcode quantity'.")

        if not order:
            print("No items in the order")
            self.customer_panel()

        total_cost = sum(item[0].price * item[1] for item in order)
        cost_transfer = total_cost
        print(f"Total cost: {total_cost}")
        use_wallet = input("Use wallet balance to pay? (yes/no): ").lower() == 'yes'
        if use_wallet and self.wallet_amount == 0:
            print("No wallet balance")
        elif use_wallet and self.wallet_amount >= total_cost:
            self.wallet_amount -= total_cost
            total_cost = 0
        elif use_wallet:
            total_cost -= self.wallet_amount
            self.wallet_amount = 0

        discount_code = input("Enter discount code if any: ")
        if discount_code.startswith("CODE10"):
            discount = DiscountCode.get_discount(discount_code)
            if discount:
                total_cost *= (1 - discount / 100)

        print(f"Final cost: {total_cost}")
        confirm = input("Confirm order? (yes/no): ").lower()
        if confirm != 'yes':
            print("Order cancelled")
            self.customer_panel()

        self.save_order(order, cost_transfer)
        print("Order placed successfully")

    def save_order(self, order, total_cost):
        order_number = self.get_next_order_number()
        user_id = self.get_user_id()
        for product, quantity in order:
            sql = """
            INSERT INTO order_history (order_history_userID, order_amount, order_number, order_history_barcodeNumber, 
            order_date, order_count, order_price_per_one )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                user_id, quantity * product.price, order_number, product.barcode, datetime.today().strftime("%Y-%m-%d"),
                quantity, product.price))
            Product.update_product_stock(product.barcode, product.stock - quantity)
        mydb.commit()
        self.wallet_amount += total_cost * 0.05
        sql = "UPDATE extrainfos SET walletAmount = %s WHERE personID = %s"
        cursor.execute(sql, (self.wallet_amount, user_id))
        mydb.commit()
        print('Saved successfully')
        self.customer_panel()

    def view_order_history(self):
        user_id = self.get_user_id()
        sql = f"""
        SELECT order_history.order_number, order_history.order_amount, products.name, order_history.order_date,
        order_history.order_count, order_history.order_price_per_one
        FROM order_history
        JOIN products ON order_history.order_history_barcodeNumber = products.BarcodeNumber
        WHERE order_history.order_history_userID = {user_id}
        ORDER BY order_history.order_number
        """
        cursor.execute(sql)
        orders = cursor.fetchall()
        if not orders:
            print("No order history")
            self.customer_panel()
        print("Order Number | Order Price | Product Name | Order Date | Order Count | Order Price per one")
        for order in orders:
            if orders.index(order) > 0:
                if order[0] != orders[orders.index(order) - 1][0]:
                    print(f"Total cost of order number{orders[orders.index(order) - 1][0]}:"
                          f" {self.returnAmountOfOrder(orders[orders.index(order) - 1][0], user_id)}")
            print(f"{order[0]} | {order[1]} | {order[2]} | {order[3]} | {order[4]} | {order[5]}")
            if orders.index(order) == len(orders) - 1:
                print(f"Total cost of order number{order[0]}:"
                      f" {self.returnAmountOfOrder(order[0], user_id)}")

        self.customer_panel()

    def returnAmountOfOrder(self, number, userID):
        sql = "SELECT SUM(order_amount) FROM order_history where (order_number=%s and order_history_userID=%s);"
        cursor.execute(sql, (number, userID))
        result = cursor.fetchone()
        return result[0]

    def change_password_customer(self):
        current_password = input('Enter current password: ')
        if current_password != self.password:
            print('Incorrect password')
            return
        new_password = input('Enter new password: ')
        if not validate_password(new_password):
            print("Password must be at least 8 characters long, include an uppercase letter, and a number.")
            return
        self.change_password(new_password)

    def charge_wallet(self):
        amount = float(input('Enter amount to charge: '))
        self.wallet_amount += amount
        sql = "UPDATE extrainfos SET walletAmount = %s WHERE personID = (SELECT personID FROM users WHERE username = " \
              "%s)"
        cursor.execute(sql, (self.wallet_amount, self.username))
        mydb.commit()
        print(f'Wallet charged successfully. New balance: {self.wallet_amount}')

    def get_next_order_number(self):
        sql = "SELECT MAX(order_number) FROM order_history WHERE order_history_userID = %s"
        cursor.execute(sql, (self.get_user_id(),))
        max_order = cursor.fetchone()[0]
        return max_order + 1 if max_order else 1

    def get_next_order_ID(self):
        sql = "SELECT MAX(orderID) FROM order_history"
        cursor.execute(sql)
        max_order = cursor.fetchone()[0]
        return max_order + 1 if max_order else 1

    def get_user_id(self):
        sql = "SELECT personID FROM users WHERE username = %s"
        cursor.execute(sql, (self.username,))
        return cursor.fetchone()[0]

    @staticmethod
    def get_all_customers():
        query = "SELECT * FROM users WHERE access = 2"
        cursor.execute(query)
        Customer.all_customers = cursor.fetchall()


class Product:
    all_products = []

    def __init__(self, product_id, name, description, price, category, stock, barcode):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.stock = stock
        self.barcode = barcode

    @staticmethod
    def get_all_products():
        query = 'SELECT productID, name, description, price, category, stock, barcodeNumber FROM products '
        cursor.execute(query)
        Product.all_products = [Product(*product) for product in cursor.fetchall()]

    @staticmethod
    def get_all_products_list():
        query = 'SELECT name, price, stock, barcodeNumber, description, category FROM products '
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    @staticmethod
    def display_all_products():
        result=Product.get_all_products_list()
        print(tabulate(result, headers=("Name", "Price", "Stock", "Barcode",  "Description", "Category")))


    @staticmethod
    def product_exists(barcode):
        Product.get_all_products()
        return any(product.barcode == barcode for product in Product.all_products)

    @staticmethod
    def get_product_by_barcode(barcode):
        Product.get_all_products()
        for product in Product.all_products:
            if product.barcode == barcode:
                return product
        return None

    @staticmethod
    def get_product_field_by_barcode(barcode, field):
        Product.get_all_products()
        for product in Product.all_products:
            if product.barcode == barcode:
                if field == 'stock':
                    return product.stock
                elif field == 'price':
                    return product.price
        return None

    @staticmethod
    def update_product(field, barcode, value):
        sql = f"UPDATE products SET {field} = %s WHERE barcodeNumber = %s"
        cursor.execute(sql, (value, barcode))
        mydb.commit()

    @staticmethod
    def update_product_stock(barcode, new_stock):
        sql = "UPDATE products SET stock = %s WHERE barcodeNumber = %s"
        cursor.execute(sql, (new_stock, barcode))
        mydb.commit()


class DiscountCode:
    @staticmethod
    def get_discount(code):
        sql = f"SELECT discountPercentage, expiryDate, used FROM discount_codes WHERE DiscountCode = %s"
        cursor.execute(sql,(code,))
        result = cursor.fetchone()
        if result:
            discount_percentage, expiry_date, used = result
            if used==1 or datetime.strptime(str(expiry_date), '%Y-%m-%d') < datetime.now():
                print("Invalid or expired discount code.")
                return 0
            sql = "UPDATE discount_codes SET used = 1 WHERE DiscountCode = %s"
            cursor.execute(sql, (code,))
            mydb.commit()
            return discount_percentage
        else:
            print("Invalid discount code.")
            return 0


def validate_password(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    return True


def check_back_to_previous(input1, input2, previous_function):
    if input1 and input1.lower() == "back" or (input2 and input2.lower() == "back"):
        previous_function()
        return True
    return False


def get_user_credentials(previous_function):
    username = input('Enter username:\n')
    if check_back_to_previous(username, None, previous_function):
        return None, None
    password = input('Enter password:\n')
    if check_back_to_previous(password, None, previous_function):
        return None, None
    return username, password


def admin_login():
    Admin.get_all_admins()
    username = input('Enter username:\n')
    if not username:
        admin_login()
    if check_back_to_previous(username, None, user_login):
        return None, None
    if User.check_username(username, 1) == False:
        print("username doesnt exist")
        admin_login()
    password = input('Enter password:\n')
    if not password:
        admin_login()
    if check_back_to_previous(password, None, user_login):
        return None, None
    if User.check_user(username, password, 1):
        admin = Admin(username, password)
        admin.admin_panel()
    else:
        print('Invalid credentials')
        admin_login()


def customer_login():
    Customer.get_all_customers()
    username = input('Enter username:\n')
    if not username:
        customer_login()
    if check_back_to_previous(username, None, customer_log):
        return None, None
    if User.check_username(username, 2) == False:
        print("username doesnt exist")
        customer_login()
    password = input('Enter password:\n')
    if not password:
        customer_login()
    if check_back_to_previous(password, None, customer_log):
        return None, None
    if Admin.check_user(username, password, 2):
        customer = Customer(username, password)
        customer.customer_panel()
    else:
        print('Invalid credentials')
        customer_login()


def customer_register():
    Customer.get_all_customers()
    username = input('Enter username:\n')
    if not username:
        return
    check_back_to_previous(username, None, customer_log)
    if any(customer[1] == username for customer in Customer.all_customers):
        print("This username already exists")
        customer_register()
        return
    password = input('Enter password:\n')
    if not password:
        return
    check_back_to_previous(password, None, customer_log)
    if not validate_password(password):
        print("Password must be at least 8 characters long, include an uppercase letter, and a number.")
        customer_register()
        return
    sql = "INSERT INTO users (username, password, access) VALUES (%s, %s, %s)"
    cursor.execute(sql, (username, password, 2))
    mydb.commit()
    sql = "INSERT INTO extrainfos (personID, walletAmount) VALUES ((SELECT personID FROM users WHERE username = %s), " \
          "%s)"
    cursor.execute(sql, (username, 0))
    mydb.commit()
    print('Successfully registered')
    customer_log()


def customer_log():
    print('1. Register')
    print('2. Sign in')
    role = input('Enter your selection\n')
    if check_back_to_previous(role, None, user_login):
        return
    if role == '1':
        customer_register()
    elif role == '2':
        customer_login()
    else:
        print("Enter valid input")
        customer_log()


def user_login():
    print('To go back to the previous step, enter the word "back"\n')
    role = input("Enter your role:\n1. Admin\n2. Customer\n")
    if check_back_to_previous(role, None, user_login):
        return
    if role == '1':
        admin_login()
    elif role == '2':
        customer_log()
    else:
        print('Enter valid input')
        user_login()


if __name__ == "__main__":
    user_login()
