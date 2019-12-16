import sqlite3
from customers.customer import customer
from customers.transaction import transaction

def open_connection():
    connection = sqlite3.connect("customers.db")
    cursor = connection.cursor()
    return connection, cursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

def create_customers_table():
    try:
        connection, cursor = open_connection()
        query = """CREATE TABLE IF NOT EXISTS customers (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_name TEXT,
                        customer_lastName TEXT,
                        transaction_id int,
                        FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id))
                    """

        cursor.execute(query)

    except sqlite3.DatabaseError as error:
        print(error)

    finally:
        close_connection(connection, cursor)

def create_transactions_table():
    try:
        connection, cursor = open_connection()
        query = """CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        transaction_number REAL,
                        customer_id int,
                        FOREIGN KEY(customer_id) REFERENCES customers(customer_id))
                    """

        cursor.execute(query)

    except sqlite3.DatabaseError as error:
        print(error)

    finally:
        close_connection(connection, cursor)

def query_database(query, params = None):
    try:
        connection, cursor = open_connection()
        if params:
            cursor.execute(query, params)
            connection.commit()
        else:
            for row in cursor.execute(query):
                print(row)

    except sqlite3.DataError as error:
        print(error)
    finally:
        connection.close()

def create_customer(customer):
    query = """INSERT INTO customers VALUES (? ,?, ?, ?)"""
    params = (customer.customer_id, customer.customer_name, customer.customer_lastName, customer.transaction_id)
    query_database(query, params)

def create_transaction(transaction, customer_id):
    query = """INSERT INTO transactions VALUES (? ,?, ?)"""
    params = (transaction.transaction_id, transaction.transaction_number, customer_id)
    query_database(query, params)

def get_customer():
    query = """SELECT * FROM customers"""
    query_database(query)

def get_transaction():
    query = """SELECT * FROM transactions"""
    query_database(query)

def update_customer(customer_id, transaction_id):
    query = """ UPDATE customers SET transaction_id = ? WHERE customer_id = ? """
    params = (transaction_id, customer_id)
    query_database (query, params)

# def update_transaction(transaction_id, customer_id):
#     query = """ UPDATE transactions SET customer_id = ? WHERE transaction_id = ? """
#     params = (transaction_id, customer_id)
#     query_database(query, params)

def insert_record(customer, transaction):
    create_customer(customer)

    connection, cursor = open_connection()

    customer_id_for_transaction = cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Irma' ").fetchone()

    close_connection(connection, cursor)

    customer.customer_id = customer_id_for_transaction[0]

    create_transaction(transaction, customer.customer_id)

    connection, cursor = open_connection()

    transaction_id_for_customer = cursor.execute("SELECT transaction_id FROM transactions ORDER BY transaction_id DESC").fetchone()

    close_connection(connection, cursor)

    transaction.transaction_id = transaction_id_for_customer[0]

    update_customer(customer.customer_id, transaction.transaction_id)


customer1 = customer(None, "Irma", "Linartaite", None)
transaction1 = transaction(None, 123456, None)

create_customers_table()
create_transactions_table()
# create_customer(customer1)
# create_transaction(transaction1)
insert_record(customer1, transaction1)
get_customer()
get_transaction()

