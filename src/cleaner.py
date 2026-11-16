import polars as pl
from detector import is_bad

columns = ['Transaction ID' , 'Item' , 'Quantity' , 'Price Per Unit' , 'Total Spent' , 'Transaction Date']
q = is_bad('Quantity')
p = is_bad('Price Per Unit')
t = is_bad('Total Spent')

def cleaning_data (data : pl.DataFrame) -> pl.DataFrame:
    """this function cleans the cafe_sales data by removing rows with bad values , casting and dropping unnecessary columns"""""
    df = (data
        .with_columns(
            pl.col(columns).cast(pl.Utf8).str.strip_chars() ,
        )
        .filter(
            ~((p & q) | (p & t) | (q & t)) ,
            ~is_bad('Item') ,
            ~is_bad('Transaction Date') ,
        )
        .drop('Payment Method' , 'Location')
        .with_columns(
            pl.col('Quantity').cast(pl.Float64 , strict = False).fill_nan(None) ,
            pl.col('Price Per Unit').cast(pl.Float64 , strict = False).fill_nan(None) ,
            pl.col('Total Spent').cast(pl.Float64 , strict = False).fill_nan(None) ,
        )
        .with_columns(
            pl.col('Quantity').fill_null(pl.col('Total Spent') / pl.col('Price Per Unit')) ,
            pl.col('Price Per Unit').fill_null(pl.col('Total Spent') / pl.col('Quantity')) ,
            pl.col('Total Spent').fill_null(pl.col('Quantity') * pl.col('Price Per Unit')) ,
        )
        .filter(
            pl.col('Quantity') > 0 ,
            pl.col('Quantity') % 1 == 0 ,
            pl.col('Price Per Unit') > 0 ,
            (pl.col('Quantity') * pl.col('Price Per Unit') - pl.col('Total Spent')).abs() < 0.01 ,
        )
        .with_columns(
            pl.col('Transaction ID').str.replace_all(r'\D' , '').cast(pl.Int64 , strict = False) ,
            pl.col('Quantity').round(0).cast(pl.Int64) ,
            pl.col('Transaction Date').str.strptime(pl.Date , '%Y-%m-%d' , strict = False) ,
            pl.col('Item').str.to_lowercase() ,
        )

        .rename({
            'Transaction ID' : 'transaction_id' ,
            'Item' : 'item' ,
            'Quantity' : 'quantity' ,
            'Price Per Unit' : 'unit_price' ,
            'Total Spent' : 'total_spent' ,
            'Transaction Date' : 'transaction_date' ,
        })
        .unique(maintain_order = True)
    )
    return df