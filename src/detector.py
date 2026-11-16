import polars as pl

columns = ['Transaction ID' , 'Item' , 'Payment Method' , 'Location' , 'Transaction Date']
anomalies = ['NULL' , 'ERROR' , 'UNKONWN' , '' , 'N/A' , 'NA' , 'NAN']

def nulls_percentage(df : pl.DataFrame) -> pl.DataFrame:
    percentages = []
    for column in columns:
        c = pl.col(column).cast(pl.Utf8).str.strip_chars().str.to_uppercase() 
        percentages.append((c.is_null() | c.is_in(anomalies)).mean().mul(100).round(2).alias(column))
    return df.select(percentages)

def is_bad(column : str) -> pl.Expr:
    c = pl.col(column).cast(pl.Utf8).str.strip_chars().str.to_uppercase() 
    return c.is_null() | c.is_in(anomalies)

def problems_QPT(df : pl.DataFrame) -> pl.DataFrame:
    q = is_bad('Quantity')
    p = is_bad('Price Per Unit')
    t = is_bad('Total Spent')
    return df.select(((p & q) | (p & t) | (q & t)).mean().mul(100).round(2).alias('Anomalies_Percentage_in_Quantity_PricePerUnit_TotalPrice'))