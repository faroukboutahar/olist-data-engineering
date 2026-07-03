select

    order_id,
    order_item_id,

    customer_id,
    product_id,

    order_purchase_timestamp,
    date(order_purchase_timestamp) as date_id,

    order_status,

    price,
    freight_value,

    price + freight_value as total_revenue,

    total_payment_value,

    customer_city,
    customer_state,

    product_category_name

from {{ ref('stg_sales_dataset') }}