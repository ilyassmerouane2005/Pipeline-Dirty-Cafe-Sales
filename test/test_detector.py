import pytest 
import polars as pl
from polars.testing import assert_frame_equal
from src.detector import nulls_percentage, is_bad, problems_QPT

data = {
    'Transaction ID': ['TXN_1961373', 'TXN_4977031', 'TXN_4271903', 'TXN_7034554', 'TXN_3160411','TXN_2602893', 'TXN_4433211', 'TXN_6699534', 'TXN_4717867'],
    'Item':            ['Coffee', 'Cake', 'Cookie', 'Salad', 'Coffee','Smoothie', 'UNKNOWN', 'Sandwich', None],
    'Quantity':        ['2', '4', '4', '2', '2', '5', '3', '4', '5'],
    'Price Per Unit':  ['2.0', '3.0', '1.0', '5.0', '2.0', '4.0', '3.0', '4.0', '3.0'],
    'Total Spent':     ['4.0', '12.0', 'ERROR', '10.0', '4.0', '20.0', '9.0', '16.0', '15.0'],
    'Payment Method':  ['Credit Card', 'Cash', 'Credit Card', 'UNKNOWN', 'Digital Wallet','Credit Card', 'ERROR', 'Cash', None],
    'Location':        ['Takeaway', 'In-store', 'In-store', 'UNKNOWN', 'In-store',None, 'Takeaway', 'UNKNOWN', 'Takeaway'],
    'Transaction Date': ['2023-09-08', '2023-05-16', '2023-07-19', '2023-04-27', '2023-06-11','2023-03-31', '2023-10-06', '2023-10-28', '2023-07-28'],
}
def test_nulls_percentage():
    """this function tests the nulls_percentage function from the detector.py file."""
    df = pl.DataFrame(data)
    result = nulls_percentage(df)
    expected = pl.DataFrame({
        'Transaction ID': [0.00],
        'Item': [22.22],
        'Payment Method': [33.33],
        'Location': [33.33],
        'Transaction Date': [0.00]
    })
    assert_frame_equal(result, expected)

def test_is_bad():
    """this function tests the is_bad function from the detector.py file."""
    df = pl.DataFrame(data)
    result1 = df.select(is_bad('Quantity')).to_series().to_list() 
    result2 = df.select(is_bad('Price Per Unit')).to_series().to_list()
    result3 = df.select(is_bad('Total Spent')).to_series().to_list()
    assert result1 == [False] * 9
    assert result2 == [False] * 9
    assert result3 == [False , False , True , False , False , False , False , False , False]

def test_problems_QPT():
    """this function tests the problems_QPT function from the detector.py file."""
    df = pl.DataFrame(data)
    result = problems_QPT(df)
    expected = pl.DataFrame({
        'Anomalies_Percentage_in_Quantity_PricePerUnit_TotalPrice': [00.00]
    })
    assert_frame_equal(result, expected)