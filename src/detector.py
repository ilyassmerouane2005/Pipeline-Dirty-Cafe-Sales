import polars as pl

columns = ['Transaction ID' , 'Item' , 'Payment Method' , 'Location' , 'Transaction Date']
anomalies = ['NULL' , 'ERROR' , 'UNKNOWN' , '' , 'N/A' , 'NA' , 'NAN']

def nulls_percentage(df : pl.DataFrame) -> pl.DataFrame:
    """ this function calculates the percentage of null values in each column of the list columns."""
    percentages = []
    for column in columns:
        c = pl.col(column).cast(pl.Utf8).str.strip_chars().str.to_uppercase() 
        percentages.append((c.is_null() | c.is_in(anomalies)).mean().mul(100).round(2).alias(column))
    return df.select(percentages)

def is_bad(column : str) -> pl.Expr:
    """ this function checks if a column contains any anomalies or null values."""
    c = pl.col(column).cast(pl.Utf8).str.strip_chars().str.to_uppercase() 
    return c.is_null() | c.is_in(anomalies)

def problems_QPT(df : pl.DataFrame) -> pl.DataFrame:
    """this function checks the problematic rows percentage in the columns Quantity, Price Per Unit and Total Spent."""
    q = is_bad('Quantity')
    p = is_bad('Price Per Unit')
    t = is_bad('Total Spent')
    return df.select(((p & q) | (p & t) | (q & t)).mean().mul(100).round(2).alias('Anomalies_Percentage_in_Quantity_PricePerUnit_TotalPrice'))