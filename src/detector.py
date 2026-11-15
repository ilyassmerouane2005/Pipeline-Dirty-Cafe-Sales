import polars as pl 

def detecting_anomalies(df: pl.DataFrame) -> pl.DataFrame:
    """
    Detects anomalies in the given Polars DataFrame.

    Args:
        df (pl.DataFrame): The input Polars DataFrame.
    Returns:
        pl.DataFrame: A DataFrame containing the anomaly rates for each column.
    """
    anomalies_rate = df.select(
            pl.col('Quantity').str.contains(r'[a-zA-Z]').mean().alias('Quantity_Anomaly_Rate') ,
            pl.col('Price Per Unit').str.contains(r'[a-zA-Z]').mean().alias('Price_Per_Unit_Anomaly_Rate') ,
            pl.col('Total Spent').str.contains(r'[a-zA-Z]').mean().alias('Total_Spent_Anomaly_Rate') ,
            pl.col('Payment Method').str.contains('UNKOWN').mean().alias('Payment_Method_Anomaly_Rate') ,
            pl.col('Location').str.contains('UNKOWN').mean().alias('Location_Anomaly_Rate') ,
            pl.col('Transaction Date').str.contains('UNKOWN').mean().alias('Transaction_Date_Anomaly_Rate') ,
    )
    return anomalies_rate

def nulls_rate (df : pl.DataFrame) -> pl.DataFrame:
    """
    Calculates the nulls rate for each column in the given Polars DataFrame.

    Args:
        df (pl.DataFrame): The input Polars DataFrame.
    Returns:
        pl.DataFrame: A DataFrame containing the nulls rates for each column.
    """
    nulls_rate = df.select(pl.all().is_null().mean()).transpose(
        include_header=True, header_name='column', column_names=['null_rate']
)
    return nulls_rate