# Thabo's Corner Store — Project Plan

## 1. Decomposition

I will break the project into smaller problems. First, I will inspect and clean the raw product and sales data. Next, I will store the cleaned data in a relational SQLite database. I will then use SQL queries and Python programming logic to analyse the sales data. After that, I will create charts to show important findings. Finally, I will add a password security gate and document the completed system.

## 2. Pattern Recognition

I expect to find several data-quality problems in the CSV files. These include missing product names, missing prices, missing quantities and payment methods, inconsistent category capitalisation, different date formats, invalid product references and duplicate records. I will look for these patterns before deciding how each issue should be handled.

## 3. Abstraction

I will focus on the information needed to answer useful business questions for Thabo, such as which products generate the most revenue and how sales change over time. I will use functions in the Python modules so that repeated tasks can be handled without writing the same code multiple times.

## 4. Algorithm / Order of Work

I will complete the project in stages. I will first clean and validate the data in `data_cleaning.py`. I will then create the SQLite database and SQL queries in `database.py`. Next, I will use functions, loops and conditionals in `analysis.py` to analyse the data. I will create the required charts in `visualize.py`, followed by the password protection in `security.py`. Finally, I will update the README with my decisions, query results, chart explanations, security reflection and key business insights.