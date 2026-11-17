import duckdb 

def clean_data_duckdb() :

    duckdb.sql (
        """
        create or replace macro is_bad(x) as
            x is null or upper(trim(cast(x as varchar))) in ('NULL','ERROR','UNKNOWN','','N/A','NA','NAN') ;
        """
    )

    clean_data = duckdb.sql (
        """
        with filtered_data as (
            select 
                trim("Transaction ID") as "transaction_id",
                lower(trim("Item")) as "item",
                trim("Quantity") as "quantity",
                trim("Price Per Unit") as "unit_price",
                trim("Total Spent") as "total_spent",
                trim("Transaction Date") as "transaction_date"
            from read_csv('data/raw/dirty_cafe_sales.csv', header=True, sep=',', all_varchar=True)
            where not is_bad("Transaction ID")
            and not is_bad("Item")
            and not (is_bad("Quantity")::int + is_bad("Price Per Unit")::int + is_bad("Total Spent")::int >= 2)
            and not is_bad("Transaction Date")
        ) ,

        transformed_data as (
            select 
                try_cast(regexp_replace(transaction_id, '\D', '' , 'g') as bigint) as transaction_id,
                item,
                try_cast(quantity as double) as quantity,
                try_cast(unit_price as double) as unit_price,
                try_cast(total_spent as double) as total_spent,
                try_cast(transaction_date as date) as transaction_date
            from filtered_data
        ) ,

        recovered_data as (
            select
                transaction_id,
                item,
                coalesce(quantity,    total_spent / unit_price) as quantity,
                coalesce(unit_price,  total_spent / quantity)   as unit_price,
                coalesce(total_spent, quantity * unit_price)    as total_spent,
                transaction_date
            from transformed_data
        ),

        final_cleaned_data as (
            select
                transaction_id,
                item,
                cast(quantity as bigint) as quantity,
                unit_price,
                total_spent,
                transaction_date
            from recovered_data
            where quantity > 0
            and quantity % 1 = 0
            and unit_price > 0
            and abs(total_spent - quantity * unit_price) < 0.01
        )
        select distinct * from final_cleaned_data
        """
    )
    return clean_data.pl()