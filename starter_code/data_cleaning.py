"""
data_cleaning.py
-----------------
Task 2: Load the raw CSV files and clean them.

This module covers KM-04 topics: Introduction to Data (data types,
errors of omission) and Data in Spreadsheets.

The raw files in data/products.csv and data/sales.csv contain REAL
data-quality problems on purpose, so you get practice fixing them:

  products.csv issues to find and fix:
    - Some products are missing a unit_price
    - One product is missing its product_name
    - Category text is inconsistently capitalised (e.g. "beverages" vs "Beverages")
    - One exact duplicate row

  sales.csv issues to find and fix:
    - sale_date is written in at least FOUR different formats
    - Some rows have a missing sale_date (an error of omission)
    - Some rows have a missing quantity
    - Some rows have a missing payment_method
    - A few rows reference a product_id that does not exist in products.csv
    - One exact duplicate row

You must handle every one of these before the data moves on to the
database in database.py. Document the decisions you make (e.g. "rows
with a missing sale_date were dropped because we cannot analyse sales
trends without a date") in your README findings section.
"""

import pandas as pd


def load_raw_data(products_path: str, sales_path: str):
    """
    Load the two raw CSV files into pandas DataFrames.

    Args:
        products_path: file path to products.csv
        sales_path: file path to sales.csv

    Returns:
        (products_df, sales_df) tuple of pandas DataFrames, UNCLEANED.
    """
    products_df = pd.read_csv(products_path)
    sales_df = pd.read_csv(sales_path)

    return products_df, sales_df


def clean_products(products_df: "pd.DataFrame") -> "pd.DataFrame":
    """
    Clean the products DataFrame.

    Must handle:
        - Missing unit_price (decide: drop the row, or fill with a sensible
          value? Justify your choice in the README.)
        - Missing product_name (a product with no name is not usable data —
          what should happen to that row?)
        - Inconsistent category capitalisation (standardise to Title Case,
          e.g. "beverages" -> "Beverages")
        - Duplicate rows (remove them)

    Returns:
        A cleaned copy of the DataFrame. Do not modify products_df in place.
    """
    cleaned = products_df.copy()
    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.dropna(subset=["product_name"])
    cleaned = cleaned.dropna(subset=["unit_price"])
    cleaned["category"] = cleaned["category"].str.title()

    return cleaned



def clean_sales(sales_df: "pd.DataFrame", valid_product_ids) -> "pd.DataFrame":
    """
    Clean sales data and standardise dates to YYYY-MM-DD.
    """
    cleaned = sales_df.copy()

    # Standardise the supported date formats explicitly.
    raw_dates = cleaned["sale_date"].astype("string").str.strip()

    parsed_dates = pd.Series(
        pd.NaT,
        index=cleaned.index,
        dtype="datetime64[ns]"
    )

    date_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
    ]

    for date_format in date_formats:
        converted = pd.to_datetime(
            raw_dates,
            format=date_format,
            errors="coerce"
        )
        parsed_dates = parsed_dates.fillna(converted)

    cleaned["sale_date"] = parsed_dates
    cleaned = cleaned.dropna(subset=["sale_date"])
    cleaned["sale_date"] = cleaned["sale_date"].dt.strftime("%Y-%m-%d")
    

    # Clean the remaining sales columns.
    cleaned["quantity"] = pd.to_numeric(
        cleaned["quantity"], errors="coerce"
    )
    cleaned = cleaned.dropna(subset=["quantity"])
    cleaned["payment_method"] = cleaned["payment_method"].fillna("Unknown")
    cleaned = cleaned[cleaned["product_id"].isin(valid_product_ids)]
    cleaned = cleaned.drop_duplicates()

    return cleaned

def cleaning_summary(raw_df: "pd.DataFrame", clean_df: "pd.DataFrame", name: str) -> str:
    """
    Build a short, human-readable string summarising how many rows were
    removed or changed during cleaning. You will paste this into your
    README findings section.

    Example output:
        "products: 16 raw rows -> 14 clean rows (2 removed)"
    """
    raw_count = len(raw_df)
    clean_count = len(clean_df)
    removed = raw_count - clean_count

    return f"{name}: {raw_count} raw rows -> {clean_count} clean rows ({removed} removed)"
