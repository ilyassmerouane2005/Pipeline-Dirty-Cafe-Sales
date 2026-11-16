import polars as pl
from src.cleaner import cleaning_data
from src.detector import is_bad

data = {
    'Transaction ID': ['TXN_1961373', 'TXN_4977031', 'TXN_4271903', 'TXN_7034554', 'TXN_3160411','TXN_2602893', 'TXN_4433211', 'TXN_6699534', 'TXN_4717867' , 'TXN_344521111'],
    'Item':            ['Coffee', 'Cake', 'Cookie', 'Salad', 'Coffee','Smoothie', 'UNKNOWN', 'Sandwich', None , 'Coffee'],
    'Quantity':        ['2', '4', '4', '2', '2', '5', '3', '4', '5' , None],
    'Price Per Unit':  ['2.0', '3.0', '1.0', '5.0', '2.0', '4.0', '3.0', '4.0', '3.0' , None],
    'Total Spent':     ['4.0', '12.0', 'ERROR', '10.0', '4.0', '20.0', '9.0', '16.0', '15.0' , '20.0'],
    'Payment Method':  ['Credit Card', 'Cash', 'Credit Card', 'UNKNOWN', 'Digital Wallet','Credit Card', 'ERROR', 'Cash', None , 'Digital Wallet'],
    'Location':        ['Takeaway', 'In-store', 'In-store', 'UNKNOWN', 'In-store',None, 'Takeaway', 'UNKNOWN', 'Takeaway' , 'In-store'],
    'Transaction Date': ['2023-09-08', '2023-05-16', '2023-07-19', '2023-04-27', '2023-06-11','2023-03-31', '2023-10-06', '2023-10-28', '2023-07-28' , '2023-08-15'],
}

def test_cleaning_data():

    df = pl.DataFrame(data)
    cleaned_df = cleaning_data(df)

    # Check that the cleaned DataFrame has the expected number of rows
    assert cleaned_df.shape[0] == 7

    # Check that the cleaned DataFrame has the expected columns
    expected_columns = ['transaction_id', 'item', 'quantity', 'unit_price', 'total_spent', 'transaction_date']
    assert list(cleaned_df.columns) == expected_columns

    # Check that there are no bad values in the cleaned DataFrame
    for column in expected_columns:
        assert not cleaned_df.select(is_bad(column)).to_series().any()

    # Check the column transaction_id 
    assert cleaned_df['transaction_id'].to_list() == [1961373, 4977031, 4271903, 7034554, 3160411, 2602893, 6699534]
    assert cleaned_df.schema['transaction_id'] == pl.Int64

    # Check the column item 
    assert cleaned_df['item'].to_list() == ['coffee', 'cake', 'cookie', 'salad', 'coffee', 'smoothie', 'sandwich']
    assert cleaned_df['item'].to_list() == cleaned_df['item'].str.strip_chars().to_list()

    # Check the column quantity
    assert cleaned_df['quantity'].to_list() == [2, 4, 4, 2, 2, 5, 4]
    assert cleaned_df.schema['quantity'] == pl.Int64

    # Check the column unit_price
    assert cleaned_df['unit_price'].to_list() == [2.0, 3.0, 1.0, 5.0, 2.0, 4.0, 4.0]
    assert cleaned_df.schema['unit_price'] == pl.Float64

    # Check the column total_spent
    assert cleaned_df['total_spent'].to_list() == [4.0, 12.0, 4.0, 10.0, 4.0, 20.0, 16.0]
    assert cleaned_df.schema['total_spent'] == pl.Float64

    # Check the column transaction_date
    assert cleaned_df.schema['transaction_date'] == pl.Date