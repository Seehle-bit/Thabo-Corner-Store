"""
database.py
------------
Task 3: Build a relational database from your cleaned data.

This module covers KM-04 topics: Introduction to Databases (DBMS,
components, characteristics) and Structured Query Language (SQL).

You will use Python's built-in `sqlite3` module — no extra install
needed. SQLite stores the whole database in a single file, which makes
it perfect for a student project (and easy to include as evidence).

By the end of this file you must be able to:
  1. Create a database file (store.db) with two related tables.
  2. Insert your cleaned data into those tables.
  3. Run at least FIVE meaningful SQL queries against the data,
     including at least one JOIN and one aggregation (SUM, COUNT, AVG).
"""

import sqlite3


def get_connection(db_path: str = "store.db") -> sqlite3.Connection:
    """
    Open (and create, if needed) the SQLite database file.

    Returns:
        an open sqlite3.Connection
    """
    return sqlite3.connect(db_path)


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create the `products` and `sales` tables if they don't already exist.

    Design requirements (this IS the relational-database design task —
    think about primary keys and foreign keys, covered in KM-04 KT04):

      products
        - product_id   TEXT, PRIMARY KEY
        - product_name TEXT, NOT NULL
        - category     TEXT
        - unit_price   REAL

      sales
        - sale_id        TEXT, PRIMARY KEY
        - product_id     TEXT, FOREIGN KEY references products(product_id)
        - quantity       INTEGER
        - sale_date      TEXT   (store as 'YYYY-MM-DD')
        - payment_method TEXT
        - customer_type  TEXT

    TODO:
        Write two CREATE TABLE IF NOT EXISTS statements (one per table)
        and execute them using conn.execute(...). Remember to call
        conn.commit() at the end.
    """
    products_sql = """
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT,
        unit_price REAL
    )
    """

    sales_sql = """
    CREATE TABLE IF NOT EXISTS sales (
        sale_id TEXT PRIMARY KEY,
        product_id TEXT,
        quantity INTEGER,
        sale_date TEXT,
        payment_method TEXT,
        customer_type TEXT,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """
    conn.execute(products_sql)
    conn.execute(sales_sql)
    conn.commit()


def insert_products(conn: sqlite3.Connection, products_df) -> None:
    """
    Insert every row of the cleaned products DataFrame into the
    products table.

    TODO:
        Loop through products_df.itertuples() (or use
        products_df.to_sql("products", conn, if_exists="append", index=False))
        and insert each row. Remember conn.commit().
    """
    for row in products_df.itertuples(index=False):
        conn.execute(
            """
            INSERT INTO products
            (product_id, product_name, category, unit_price)
            VALUES (?, ?, ?, ?)
            """,
            (row.product_id, row.product_name, row.category, row.unit_price)
        )

    conn.commit()


def insert_sales(conn: sqlite3.Connection, sales_df) -> None:
    """
    Insert every row of the cleaned sales DataFrame into the sales table.

    TODO: same approach as insert_products().
    """
    for row in sales_df.itertuples(index=False):
        conn.execute(
            """
            INSERT INTO sales
            (sale_id, product_id, quantity, sale_date, payment_method, customer_type)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row.sale_id,
                row.product_id,
                row.quantity,
                row.sale_date,
                row.payment_method,
                row.customer_type
            )
        )

    conn.commit()


# ---------------------------------------------------------------------
# SQL QUERIES — write at least FIVE for your project.
# Three are started for you below; you must complete them and add TWO
# more of your own that answer a business question you find interesting.
# ---------------------------------------------------------------------

def query_total_revenue_per_product(conn: sqlite3.Connection):
    """
    Return each product's name and its total revenue
    (quantity * unit_price, summed across all its sales),
    highest revenue first.

    TODO: write a SQL query that JOINS sales to products on product_id,
    multiplies quantity * unit_price, and uses SUM() with GROUP BY.
    Execute it with conn.execute(sql) and return conn.execute(sql).fetchall()
    """
    sql = """
    SELECT
        products.product_name,
        SUM(sales.quantity * products.unit_price) AS total_revenue
    FROM sales
    JOIN products
        ON sales.product_id = products.product_id
    GROUP BY products.product_id, products.product_name
    ORDER BY total_revenue DESC
    """

    return conn.execute(sql).fetchall()


def query_best_selling_product(conn: sqlite3.Connection):
    """
    Return the single best-selling product by total quantity sold.

    TODO: use JOIN, SUM(), GROUP BY, ORDER BY and LIMIT 1.
    """
    sql = """
    SELECT
        products.product_name,
        SUM(sales.quantity) AS total_quantity
    FROM sales
    JOIN products
        ON sales.product_id = products.product_id
    GROUP BY products.product_id, products.product_name
    ORDER BY total_quantity DESC
    LIMIT 1
    """

    return conn.execute(sql).fetchall()


def query_sales_by_payment_method(conn: sqlite3.Connection):
    """
    Return the number of sales for each payment method.

    TODO: use COUNT() and GROUP BY.
    """
    sql = """
    SELECT
        payment_method,
        COUNT(*) AS total_sales
    FROM sales
    GROUP BY payment_method
    ORDER BY total_sales DESC
    """

    return conn.execute(sql).fetchall()


def query_custom_one(conn: sqlite3.Connection):
    """
    Custom business question:
    Which product category generates the most revenue?
    """
    sql = """
    SELECT
        products.category,
        SUM(sales.quantity * products.unit_price) AS total_revenue
    FROM sales
    JOIN products
        ON sales.product_id = products.product_id
    GROUP BY products.category
    ORDER BY total_revenue DESC
    """

    return conn.execute(sql).fetchall()


def query_custom_two(conn: sqlite3.Connection):
    """
    Custom business question:
    How many sales were made to each customer type?
    """
    sql = """
    SELECT
        customer_type,
        COUNT(*) AS total_sales
    FROM sales
    GROUP BY customer_type
    ORDER BY total_sales DESC
    """

    return conn.execute(sql).fetchall()
