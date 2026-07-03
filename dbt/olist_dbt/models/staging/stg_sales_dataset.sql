select *
from {{ source('analytics', 'sales_dataset') }}