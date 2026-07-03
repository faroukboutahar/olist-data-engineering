select
    date_id,

    count(distinct order_id) as nb_commandes,

    round(sum(price), 2) as ca_produits,
    round(sum(freight_value), 2) as ca_transport,
    round(sum(total_revenue), 2) as ca_total,


from {{ ref('fact_sales') }}

group by date_id