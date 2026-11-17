# ☕ Cafe Sales Data Cleaning Pipeline

A data cleaning and quality assessment pipeline for a dirty cafe sales dataset, implemented using **Polars** and **DuckDB**.

This project detects data quality issues, analyzes missing and invalid values, cleans inconsistent records, recovers missing numerical values, and exports the cleaned data into two different formats: **Parquet** using Polars and **SQLite** using DuckDB and SQL.

The project demonstrates two approaches to data processing: DataFrame-based transformations with Polars and SQL-based transformations with DuckDB.

## 🚀 Project Overview

Real-world datasets often contain missing values, inconsistent formats, invalid entries, and numerical inconsistencies.

The goal of this project is to build a pipeline that processes a dirty cafe sales CSV dataset and produces clean, structured, and reliable data.

The pipeline follows these main steps:

1. **Extract:** Load the raw CSV dataset using Polars.
2. **Detect:** Identify missing values and anomalies using Polars and SQL with DuckDB.
3. **Analyze:** Calculate the percentage of missing or problematic values.
4. **Clean:** Remove invalid records, standardize data, convert data types, and recover missing numerical values.
5. **Export:** Save the cleaned Polars DataFrame as a Parquet file and the DuckDB SQL cleaning result as a table in an SQLite database.

## 🛠️ Technologies Used

- **Python:** Main programming language.
- **Polars:** Fast DataFrame processing, data quality detection, and data cleaning.
- **DuckDB:** SQL-based data analysis and cleaning.
- **SQLite:** Storage for the cleaned `cafe_sales` table.
- **Parquet:** Columnar storage format for the cleaned Polars dataset.
- **Pytest:** Unit testing.

## 📂 Project Structure

```text
cafe-sales-data-cleaning/
│
├── data/
│   ├── raw/
│   │   └── dirty_cafe_sales.csv
│   │
│   └── processed/
│       ├── cafe_sales_cleaned.parquet
│       └── cafe.db
│
├── src/
│   ├── __init__.py
│   ├── extractor.py
│   ├── detector.py
│   ├── detector_duckdb.py
│   ├── cleaner.py
│   └── cleaner_duckdb.py
│
├── test/
│   ├── __init__.py
│   ├── test_detector.py
│   └── test_cleaner.py
│
├── main.py
├── requirements.txt
├── pytest.ini
└── .gitignore
```

## 🔍 Data Quality Detection

The pipeline considers the following values as missing or invalid:

- `NULL`
- `ERROR`
- `UNKNOWN`
- Empty strings
- `N/A`
- `NA`
- `NAN`
- Actual null values

### 1. Detection with Polars

The `detector.py` module provides three functions:

- **`is_bad(column)`**: Identifies missing or invalid values in a specified column.
- **`nulls_percentage(df)`**: Calculates the percentage of missing or invalid values in each selected categorical and identification column.
- **`problems_QPT(df)`**: Calculates the percentage of problematic rows where at least two of the following columns contain invalid values:
  - Quantity
  - Price Per Unit
  - Total Spent

### 2. Detection with DuckDB

The `detector_duckdb.py` module performs similar data quality checks using SQL.

It defines an `is_bad()` SQL macro and calculates the percentage of missing values in individual columns, as well as the percentage of rows with multiple anomalies in Quantity, Price Per Unit, and Total Spent.

## 🧹 Data Cleaning

The project implements two independent cleaning approaches.

### 1. Cleaning with Polars

Implemented in `cleaner.py`, the `cleaning_data()` function performs the following operations:

- Removes unnecessary whitespace from values.

- Removes rows with invalid Transaction IDs, Items, or Transaction Dates.

- Removes rows where at least two of the three numerical columns (Quantity, Price Per Unit, Total Spent) are missing or invalid.

- Drops the `Payment Method` and `Location` columns because both contain more than 30% anomalies. These columns are also not essential to the main cafe sales analysis.

- Converts numerical columns to appropriate data types.

- Recovers missing numerical values using mathematical relationships:

  **Total Spent = Quantity × Price Per Unit**

  - Missing Quantity = Total Spent / Price Per Unit
  - Missing Price Per Unit = Total Spent / Quantity
  - Missing Total Spent = Quantity × Price Per Unit

- Removes records with non-positive quantities or prices.

- Ensures Quantity is a positive integer.

- Checks the consistency of Total Spent with Quantity × Price Per Unit, allowing a tolerance of less than 0.01.

- Extracts numeric digits from Transaction IDs.

- Converts Transaction Date into a Date type.

- Converts Item values to lowercase.

- Renames columns to lowercase snake_case.

- Removes duplicate records.

### 2. Cleaning with DuckDB

Implemented in `cleaner_duckdb.py`, the `clean_data_duckdb()` function reproduces the cleaning process using SQL.

It uses Common Table Expressions (CTEs) to organize the transformations into four stages:

1. **`filtered_data`**: Filters invalid records and standardizes the raw values.
2. **`transformed_data`**: Converts values into appropriate SQL data types using `TRY_CAST`.
3. **`recovered_data`**: Recovers missing numerical values using `COALESCE`.
4. **`final_cleaned_data`**: Applies numerical validation and returns distinct cleaned records.

Finally, the resulting DuckDB relation is converted into a Polars DataFrame.

## 📤 Data Export

The pipeline produces two cleaned outputs from two different implementations.

| Implementation | Output                       | Format                    |
| -------------- | ---------------------------- | ------------------------- |
| Polars         | `cafe_sales_cleaned.parquet` | Parquet                   |
| DuckDB         | `cafe_sales`                 | SQLite table in `cafe.db` |

Both outputs contain the cleaned cafe sales data with the following columns:

| Column             | Data Type | Description                    |
| ------------------ | --------- | ------------------------------ |
| `transaction_id`   | Integer   | Numeric transaction identifier |
| `item`             | String    | Cafe product name              |
| `quantity`         | Integer   | Number of items purchased      |
| `unit_price`       | Float     | Price per item                 |
| `total_spent`      | Float     | Total transaction amount       |
| `transaction_date` | Date      | Transaction date               |

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

cd YOUR_REPOSITORY
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**

```bash
.venv\Scripts\activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the dataset

Place the raw CSV file inside:

```text
data/raw/dirty_cafe_sales.csv
```

Make sure the `data/processed/` directory exists before running the pipeline.

## ▶️ Running the Pipeline

Run the main script from the project root:

```bash
python main.py
```

The script will:

1. Extract the raw CSV data.
2. Clean the data using Polars.
3. Export the Polars result to a Parquet file.
4. Clean the data using DuckDB and SQL.
5. Export the DuckDB result into the `cafe_sales` table in an SQLite database.

## 🧪 Running Tests

The project uses Pytest to validate the detection and cleaning functions implemented with Polars.

Run all tests using:

```bash
pytest
```

The tests cover:

- Missing-value percentage calculations.
- Invalid-value detection.
- Numerical anomaly detection.
- Data cleaning and row filtering.
- Numerical value recovery.
- Column names and data types.
- Transaction ID and Item transformations.

## 📌 Important Assumptions

The cleaning logic relies on several assumptions:

- A row is considered recoverable when no more than one of Quantity, Price Per Unit, and Total Spent is invalid.
- At least two valid numerical values are needed to recover the third.
- Quantity must be a positive integer.
- Price Per Unit must be positive.
- Total Spent must be mathematically consistent with Quantity multiplied by Price Per Unit, within a tolerance of 0.01.
- Transaction IDs contain numeric digits that can be extracted.
- Transaction dates follow the `YYYY-MM-DD` format.
- Payment Method and Location are excluded because they contain more than 30% anomalies and are not essential to the main analysis.

## 🎯 Project Goals

This project aims to demonstrate practical data engineering and data quality concepts:

- Handling dirty CSV datasets.
- Detecting missing values and anomalies.
- Applying data validation rules.
- Recovering missing numerical values.
- Performing transformations using both Polars and SQL.
- Working with DuckDB and SQLite.
- Exporting data into analytical storage formats such as Parquet.
- Writing unit tests for data processing functions.

---

**Author:** Ilyass Merouane

**Technologies:** Python · Polars · DuckDB · SQL · SQLite · Parquet · Pytest
