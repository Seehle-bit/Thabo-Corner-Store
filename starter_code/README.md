# Thabo's Corner Store — Sales Insights System (Starter Code)

This is your starting scaffold. It already contains the **shape** of the
project — file structure, function signatures, imports and docstrings —
so you can focus on the actual data, database and programming logic
described in the Project Brief.

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

1. Make sure Python 3.10+ is installed: `python3 --version`
2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the `data/` folder (provided separately) so it sits **next to**
   `starter_code/`, like this:
   ```
   project/
   ├── data/
   │   ├── products.csv
   │   └── sales.csv
   └── starter_code/
       └── ... (these files)
   ```

## Running your program

Once you've completed the TODOs in each file:

```bash
python main.py
```

## A note on the TODOs

Every function you need to complete has:
- A docstring explaining **what** it must do
- A `# TODO:` comment explaining **the specific steps**
- `raise NotImplementedError` as a placeholder — delete this once you've
  written your own code

Do not change the function names or the arguments they accept —
`main.py` calls them by name, and your facilitator's marking checklist
also references these exact names.

Good luck — and remember to commit your progress to GitHub regularly
as you complete each task, not just once at the end!

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