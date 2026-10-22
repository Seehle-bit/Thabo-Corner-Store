# Thabo's Corner Store — Sales Insights System

An integrated AI Software Development project combining data cleaning, SQLite databases, SQL queries, Python programming, data visualisation and basic security.

**Project modules:** KM-04 Data & Databases and KM-05 Programming & Python

**Tools:** Python, pandas, SQLite, SQL and Matplotlib


## Project Overview

Thabo's Corner Store — Sales Insights System is a completed integrated learning project for the Occupational Certificate: Artificial Intelligence Software Developer, NQF Level 4. It combines KM-04 Data & Databases with KM-05 Programming & Python.

The application processes raw product and sales CSV files, cleans data-quality issues, stores validated records in a relational SQLite database, runs SQL queries, analyses sales patterns using Python, generates charts with Matplotlib, and demonstrates a password-hashing login gate.

The project was developed in stages using computational thinking, modular programming, data validation, and Git version control. It is an educational prototype designed to demonstrate core software development and data analysis skills, not a production-ready retail system.

## Running the Program

From the main project folder, open PowerShell and install the dependencies:

```powershell
python -m pip install -r starter_code/requirements.txt
```

Run the complete application:

```powershell
python starter_code/main.py
```

The program loads the raw CSV files, cleans the data, builds and queries the SQLite database, performs sales analysis, and generates the following chart files:

- `revenue_per_product.png`
- `monthly_trend.png`

Python 3.10 or later is required. The project uses pandas, Matplotlib, and Python's built-in SQLite support.

## Folder structure

```
starter_code/
├── README.md              <- this file
├── requirements.txt        <- Python packages you need
├── main.py                 <- entry point; runs your whole pipeline
├── data_cleaning.py         <- Task 2: load & clean the raw CSVs
├── database.py              <- Task 3: build the SQLite database + SQL queries
├── analysis.py               <- Task 4: functions/loops/conditionals for insights
├── visualize.py               <- Task 5: charts with matplotlib
└── security.py                 <- Task 6: simple login / password hashing
```

## Before you start

### Requirements
- Python 3.10 or later
- pandas
- matplotlib
- SQLite (included with Python's `sqlite3` module)

### Install dependencies

Open PowerShell in the main project folder and run:

```powershell
python -m pip install -r starter_code/requirements.txt
```

The raw data files should be located in the `data/` folder alongside `starter_code/`.

Expected structure:

```text
Thabo-Corner-Store/
├── data/
│   ├── products.csv
│   └── sales.csv
└── starter_code/
    ├── requirements.txt
    ├── main.py
    └── ...
```


## Task 2 — Data Cleaning Findings

### Products

The raw products data contained 16 rows. During cleaning, 4 rows were removed, leaving 12 clean rows.

The following cleaning decisions were made:

- Exact duplicate rows were removed.
- Rows with a missing `product_name` were removed because a product without a name cannot be reliably identified.
- Rows with a missing `unit_price` were removed because the correct price could not be determined without guessing.
- Category names were standardised using Title Case so that values such as `beverages` and `Beverages` use a consistent format.

### Sales

The raw sales data contained 71 rows. After cleaning, 43 rows remained.

The following cleaning decisions were made:

- Sale dates were converted from the different formats found in the raw data into the standard `YYYY-MM-DD` format.
- Rows with missing or unparseable sale dates were removed because sales trends cannot be analysed reliably without a date.
- Rows with missing quantities were removed because a sale without a quantity cannot be used reliably for sales calculations.
- Missing payment methods were changed to `Unknown` rather than guessing the payment method.
- Sales records referencing product IDs that did not exist in the cleaned products data were removed.
- Exact duplicate sales rows were removed.

After cleaning, the data contained no missing sale dates, quantities or payment methods, no invalid product IDs and no duplicate rows.

**Date-format handling:** Sale dates were parsed using pandas with `format="mixed"` and `errors="coerce"`. Values that could not be parsed were treated as missing and removed. Valid dates were then standardised to `YYYY-MM-DD`. Some date strings can be interpreted in more than one way, so ambiguous dates must be checked against the source format or an agreed date convention before the results are treated as definitive.

## Task 3 — Database and SQL

### Database Design

A SQLite relational database named `store.db` was created using Python's built-in `sqlite3` module.

The database contains two related tables:

- `products` — stores product information such as product ID, name, category and unit price.
- `sales` — stores sales information such as sale ID, product ID, quantity, sale date, payment method and customer type.

The `product_id` field in the `products` table is the primary key. The `sale_id` field in the `sales` table is the primary key. The `product_id` field in the `sales` table is a foreign key that references the `products` table.

### SQL Queries and Results

#### 1. Total revenue per product

The first query joins the `sales` and `products` tables and calculates revenue using quantity multiplied by unit price.

The highest-revenue products were:

- 5kg Maize Meal — R801.00
- Eggs (6 pack) — R364.00
- Bar One Chocolate — R224.00

**Data-quality finding: duplicate product names**

The raw products data contained two records for Coca-Cola 500ml, with product IDs `P001` and `P015`. Both records had the same category and unit price, but both IDs were referenced in the sales data.

Rather than deleting a product record or rewriting historical sales, the revenue query was updated to group results by `product_name`. This combines revenue from both IDs into one report entry, showing total Coca-Cola 500ml revenue of **R222.00** in the cleaned dataset.

The original product IDs remain unchanged in the source data and database. This reporting decision combines products with identical names; in a real business system, duplicate records should be investigated to confirm whether they represent the same product before merging inventory or master records.

#### 2. Best-selling product

The query calculated the total quantity sold for each product.

**Bar One Chocolate** was the best-selling product by quantity, with **16 units sold**.

#### 3. Sales by payment method

The number of sales for each payment method was:

- Cash : 14
- Mobile Money : 11
- Card : 10
- Unknown : 8

Cash was the most common payment method.

#### 4. Revenue by product category

The custom query calculated the total revenue generated by each product category.

The highest-revenue categories were:

- Household : R1,021.50
- Dairy : R493.00
- Snacks : R356.00
- Beverages : R333.00
- Airtime & Data : R238.00
- Bakery : R48.00

Household products generated the highest total revenue.

#### 5. Sales by customer type

The custom query counted the number of sales for each customer type:

- Walk-in : 18
- Regular : 15
- Missing/Unknown : 10

The missing customer-type values were not guessed or changed because there was no reliable information available to determine the correct customer type.

## Task 4 — Python Programming and Sales Analysis

Python functions were developed to analyse the cleaned sales and product data using loops, conditionals and data structures.

### 1. Total sales records

The `total_sales_records()` function counts the number of cleaned sales records. The cleaned dataset contained **43 sales records**.

### 2. Low-stock alert

The `low_stock_alert()` function identifies products that are marked as out of stock. The analysis flagged **Data Bundle 1GB** for attention.

### 3. Monthly sales trend

The `monthly_sales_trend()` function groups sales quantities by month to support trend analysis. The cleaned dataset showed sales activity in January and February 2026, with monthly totals of 52 and 44 units respectively. These results reflect the available cleaned records and should not be interpreted as a complete record of every month of the year.

### 4. Transaction-size classification

The `classify_transaction_size()` function uses conditional statements to classify transactions:

- Quantity of 1: `Single`
- Quantities from 2 to 4: `Multiple`
- Quantity of 5 or more: `Bulk`
- Quantity of 0 or less: `Invalid`

### 5. Average basket size

The `average_basket_size()` function calculates the average quantity per sales record. The result was approximately **2.23 units per record**.

These functions demonstrate how Python can transform cleaned data into information that supports store operations and decision-making.

## Task 5 — Data Visualisation

Two charts were generated using Matplotlib to make the sales analysis easier to understand.

### 1. Revenue per product

The bar chart, saved as `revenue_per_product.png`, compares revenue generated by individual products. It helps the store owner identify products contributing the most revenue and compare their performance.

### 2. Monthly sales trend

The line chart, saved as `monthly_trend.png`, displays total quantities sold across the months represented in the cleaned dataset. It helps the store owner observe changes in sales activity over time.

Both charts were saved as PNG files so they can be viewed independently and included as project evidence.

## Task 6: Security and the CIA Triad

### 1. Confidentiality

Confidentiality means protecting information from unauthorised access. In this project, the login system requires a password before users can access the sales reports. Password hashing is demonstrated to avoid storing the password directly in plain text. However, this is an educational prototype, not a production-ready security system. SHA-256 alone is not recommended for production password storage, and a hardcoded password creates additional security risks. A real system should use a dedicated password-hashing algorithm and securely managed credentials.

### 2. Integrity

Integrity means keeping data accurate, complete and consistent. The SQLite database uses primary keys to identify records, while product IDs connect sales records to products. The data-cleaning process removes duplicate records, handles missing values and removes sales linked to invalid product IDs. These checks help prevent unreliable data from affecting sales calculations and business reports. Database constraints and validation should also be maintained when new records are added.

### 3. Availability

Availability means ensuring that authorised users can access information when needed. If the database is stored on one computer, hardware failure, theft or accidental deletion could make reports unavailable. Regular backups to a secure external drive or trusted cloud storage would help recover important information. Backup files should be protected from unauthorised access, and restoration should be tested regularly. These backup and recovery measures are recommendations for improving the project; they are not currently implemented as an automated feature.

## Task 7 — Key Business Insights and Recommendations

The analysis provides several useful findings for Thabo's Corner Store.

First, 5kg Maize Meal generated the highest revenue among the listed products, at R801.00. Eggs (6 pack) generated R364.00, while Bar One Chocolate generated R224.00. The store owner could monitor the availability of these products and investigate whether customer demand remains consistent. Revenue alone does not show profit, so product costs would be needed before deciding which products are most profitable.

Second, Bar One Chocolate was the best-selling product by quantity, with 16 units sold. This suggests that it may be a popular item. Thabo could monitor its stock levels and consider customer demand when planning replenishment.

Third, cash was the most common recorded payment method, with 14 sales, followed by mobile money with 11 and card payments with 10. Thabo should continue supporting the payment methods customers use while monitoring whether these preferences change.

Fourth, Household products generated the highest category revenue, at R1,021.50. The store owner could review the household product range and compare revenue with purchasing costs to understand its contribution to profit.

Finally, 10 sales records had missing customer-type information, and eight had an unknown payment method. Improving data collection could make future reports more reliable. The monthly trend also contains gaps, so additional complete sales records would help provide a clearer picture of seasonal patterns.

Overall, the system demonstrates how data cleaning, SQL queries, Python analysis and visualisation can help a small business make more informed decisions about stock, sales and record keeping.