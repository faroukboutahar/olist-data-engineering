with date_spine as (

    select date_day
    from unnest(
        generate_date_array(
            (select min(date(order_purchase_timestamp)) from {{ ref('fact_sales') }}),
            (select max(date(order_purchase_timestamp)) from {{ ref('fact_sales') }}),
            interval 1 day
        )
    ) as date_day

)

select
    date_day as date_id,
    extract(year from date_day) as year,
    extract(month from date_day) as month,
    format_date('%B', date_day) as month_name,
    extract(quarter from date_day) as quarter,
    extract(week from date_day) as week,
    extract(day from date_day) as day,
    format_date('%A', date_day) as day_name,
    case
        when extract(dayofweek from date_day) in (1, 7) then true
        else false
    end as is_weekend

from date_spine