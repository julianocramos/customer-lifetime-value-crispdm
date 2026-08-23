# Case Questions and Answers

## 1. How does LTV vary by entry product?

**Lifetime Access** has the highest average LTV at approximately **R$ 4,980.48**, but it represents only about **4.15% of customers**.

When customer volume is included, the largest contributors to total historical LTV are:

- **Python:** 11,444 customers | average LTV **R$ 2,097.22** | total LTV **R$ 24,000,592.46**
- **Community:** 10,827 customers | average LTV **R$ 1,778.27** | total LTV **R$ 19,253,351.38**
- **Power BI:** 6,971 customers | average LTV **R$ 2,378.33** | total LTV **R$ 16,579,320.09**

**Conclusion:** the product with the highest LTV per customer is not necessarily the product that creates the most total economic value. Product decisions should combine **average LTV and customer volume**.

## 2. How does LTV vary by sales strategy?

**Other** and **Commercial** have the highest average historical LTVs, at approximately **R$ 2.52k**, but both have relatively low customer volume.

**Launch** represents **29,998 customers** and generates approximately **R$ 65.65M in total historical LTV**, making it the most economically relevant sales strategy by scale.

Direct channel comparisons can be confounded by variables such as:

- first-purchase value;
- entry-product mix;
- recurring versus non-recurring first purchase.

**Conclusion:** a channel should not be judged only by average LTV. Scale materially changes the business interpretation.

## 3. Do customers with a recurring first purchase have the same LTV as non-recurring customers?

No.

- **Non-recurring:** 22,529 customers | average LTV **R$ 3,004.93** | total LTV **R$ 67,698,074.34**
- **Recurring:** 16,224 customers | average LTV **R$ 1,064.27** | total LTV **R$ 17,266,741.88**

The groups also differ sharply in average first-purchase value:

- non-recurring: **R$ 1,153.99**
- recurring: **R$ 108.20**

In the multivariate linear model, recurrence is associated with approximately **R$ 369 lower predicted LTV**, holding the other model variables constant.

**Conclusion:** the historical difference is substantial, but it should not be interpreted as causal. First-purchase value, observation window, and the operational definition of LTV all affect interpretation.

## 4. How can LTV prediction support media-investment decisions?

The selected **Linear Regression** model achieved:

- **R²:** 0.8478
- **RMSE:** R$ 507.74
- **MAE:** R$ 404.03

The model uses only information available at the first purchase, so it can generate an expected LTV for new customers before future behavior is observed.

The prediction can support:

- prioritizing higher-value customer segments;
- comparing products and acquisition channels;
- setting differentiated acquisition limits;
- combining expected LTV with contribution margin, risk, payback, and uncertainty to define a maximum acceptable CAC.

**Conclusion:** predicted LTV should be treated as a decision-support estimate, not as a guaranteed future value.
