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

create_customers_table()

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

create_transactions_table()

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
    query = """INSERT INTO customers VALUES (? ,?, ?)"""
    params = (customer.customer_id, customer.customer_name, customer.customer_lastName)
    query_database(query, params)

customer1 = customer(None, "Irma", "Linartaite")

create_customer(customer1)

def create_transaction(transaction):
    query = """INSERT INTO transactions VALUES (? ,?)"""
    params = (transaction.transaction_id, transaction.transaction_number)
    query_database(query, params)

transaction1 = transaction(None, 123456)

create_transaction(transaction1)

def get_customer(customer):
    query = """SELECT * FROM customers"""
    query_database(query)

get_customer(customer1)

def get_transaction(transaction):
    query = """SELECT * FROM transactions"""
    query_database(query)

get_transaction(transaction1)