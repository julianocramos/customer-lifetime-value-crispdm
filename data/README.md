# Data

The original educational dataset is **not redistributed in this repository**.

The original prepared dataset uses Portuguese column names and category labels. The Python pipeline translates that source schema into the English modeling schema below:

- `first_purchase_value`
- `recurring_first_purchase`
- `entry_product`
- `sales_channel`
- `gender`
- `education`
- `purchase_month`
- `purchase_day_of_week`
- `LTV` (target)

To reproduce the original metrics, place the authorized prepared dataset locally at:

```text
data/ltv_base_tratada_cardinalidade_final.csv
```

The file `sample_input_template.csv` is an **illustrative English-language input template** for new-customer scoring. It is not part of the original dataset.
