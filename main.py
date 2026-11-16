import polars as pl
from src.extractor import extract_data
from src.cleaner import cleaning_data

def main():
    raw_data = extract_data()
    clean_data = cleaning_data(raw_data)
    clean_data.write_parquet('data/processed/cafe_sales_cleaned.parquet')