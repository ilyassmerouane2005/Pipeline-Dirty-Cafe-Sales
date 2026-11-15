import polars as pl

def extract_data (path : str = 'data/raw/dirty_cafe_sales.csv') -> pl.DataFrame:
    """
    Extracts data from a CSV file and returns it as a Polars DataFrame.

    Args:
        path (str): The file path to the CSV file. Defaults to 'data/raw/dirty_cafe_sales.csv'.

    Returns:
        pl.DataFrame: The extracted data as a Polars DataFrame.
    """
    return pl.read_csv(path)