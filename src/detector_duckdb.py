import duckdb

def detect_missing_values():
    """this function detects the anomalies in each column of the csv ile dirty_cafe_sales.csv and returns the percentage of missing values in each column."""
    duckdb.sql ("""
        create or replace macro is_bad(x) as
            x is null or upper(trim(cast(x as varchar))) in ('NULL','ERROR','UNKNOWN','','N/A','NA','NAN') ;
    """
    )

    missing_values = duckdb.sql("""
        select 
            round(avg(is_bad("Transaction ID")::int) * 100 , 2) as TransactionID_missing_percentage,
            round(avg(is_bad("Item")::int) * 100 , 2) as Item_missing_percentage,
            round(avg(is_bad("Payment Method")::int) * 100 , 2) as Payment_Method_missing_percentage,
            round(avg(is_bad("Location")::int) * 100 , 2) as Location_missing_percentage,
            round(avg(is_bad("Transaction Date")::int) * 100 , 2) as Transaction_Date_missing_percentage,
            round(avg((is_bad("Quantity")::int + is_bad("Price Per Unit")::int + is_bad("Total Spent")::int >= 2)::int) * 100, 2) as Anomalies_Per_in_QPT
        from read_csv('data/raw/dirty_cafe_sales.csv', header=True, sep=',', all_varchar=True)
    """)

    return missing_values.show()