import polars as pl
from src.extractor import extract_data
from src.cleaner import cleaning_data
from src.cleaner_duckdb import clean_data_duckdb

def main():
    raw_data = extract_data()
    clean_data = cleaning_data(raw_data)
    clean_data.write_parquet('data/processed/cafe_sales_cleaned.parquet')
    data = clean_data_duckdb()
    data.write_database('cafe_sales', connection='sqlite:///data/processed/cafe.db', engine='adbc', if_table_exists='replace')

if __name__ == "__main__":
    main()