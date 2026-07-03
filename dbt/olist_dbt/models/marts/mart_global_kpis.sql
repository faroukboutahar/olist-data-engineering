select
    round(sum(total_revenue), 2) as ca_total,
    count(distinct order_id) as nb_commandes,
    round(sum(total_revenue) / count(distinct order_id), 2) as panier_moyen

from {{ ref('fact_sales') }}