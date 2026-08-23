import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Customer LTV Simulator",
    page_icon="📈",
    layout="wide",
)

# -------------------------------------------------------------------
# Model parameters
# These values are the fitted parameters of the selected Linear Regression
# model used in the portfolio project. They allow the demo to run without
# redistributing the original educational dataset.
# -------------------------------------------------------------------

INTERCEPT = 2747.8860654835735
FIRST_PURCHASE_MEAN = 715.1107747634687
FIRST_PURCHASE_SCALE = 665.9064613725793
FIRST_PURCHASE_COEF = 1013.2873103571518
RECURRING_COEF = -368.7296916216356

TEST_R2 = 0.8477576423540136
TEST_RMSE = 507.73530215899626
TEST_MAE = 404.0261679823802

COEFFICIENTS = {
    "entry_product": {
        "Commercial": 0.0,
        "Community": -306.13934499170807,
        "Data Analysis": -155.9120117547081,
        "Data Science": 91.26021762208455,
        "Excel": -253.36933078605395,
        "Full Stack JavaScript": -107.6436041491745,
        "Lifetime Access": 354.02343969186836,
        "Other": -193.3406707514381,
        "Power BI": 36.018635174877765,
        "Python": -157.04202564378025,
    },
    "sales_channel": {
        "Checkout": 0.0,
        "Commercial": -138.72997200847198,
        "Direct Traffic": -528.614588328954,
        "Launch": -211.39336687705062,
        "Other": -614.4626460042267,
        "Waitlist": -412.80729030685717,
        "Webinar": -169.99012372592279,
    },
    "gender": {
        "Female": 0.0,
        "Male": 9.714148867380832,
        "Other": 7.747227096851855,
    },
    "education": {
        "Basic Education": 0.0,
        "High School": -26.868855007722686,
        "Higher Education - Complete": -17.382228134447868,
        "Higher Education - Incomplete": -24.013084058009756,
        "Higher Education+": -23.84950788554162,
        "Not Reported": -27.92384865699283,
    },
    "purchase_month": {
        1: 0.0,
        2: 6.823636153664222,
        3: 7.9287154060584735,
        4: 11.615456819275723,
        5: -25.72489275593819,
        6: 11.264137525624022,
        7: -12.462186386139905,
        8: -28.91453218494131,
        9: 23.72690737288671,
        10: 12.534944008951202,
        11: 22.69886648362883,
        12: 13.72426878021508,
    },
    "purchase_day_of_week": {
        "Friday": 0.0,
        "Monday": -4.071061642523554,
        "Saturday": 6.2257800857395,
        "Sunday": 2.0766874335308954,
        "Thursday": -12.426676794120015,
        "Tuesday": 9.222414228021588,
        "Wednesday": -6.058396875396041,
    },
}


def brl(value: float) -> str:
    """Format a number as Brazilian reais for display."""
    formatted = f"{value:,.2f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


def predict_ltv(
    first_purchase_value: float,
    recurring: bool,
    entry_product: str,
    sales_channel: str,
    gender: str,
    education: str,
    purchase_month: int,
    purchase_day_of_week: str,
):
    standardized_purchase = (
        first_purchase_value - FIRST_PURCHASE_MEAN
    ) / FIRST_PURCHASE_SCALE

    contributions = {
        "Model baseline": INTERCEPT,
        "First purchase value": FIRST_PURCHASE_COEF * standardized_purchase,
        "Recurring first purchase": RECURRING_COEF if recurring else 0.0,
        "Entry product": COEFFICIENTS["entry_product"][entry_product],
        "Sales channel": COEFFICIENTS["sales_channel"][sales_channel],
        "Gender": COEFFICIENTS["gender"][gender],
        "Education": COEFFICIENTS["education"][education],
        "Purchase month": COEFFICIENTS["purchase_month"][purchase_month],
        "Purchase day": COEFFICIENTS["purchase_day_of_week"][purchase_day_of_week],
    }

    prediction = sum(contributions.values())
    return prediction, contributions


st.title("Customer Lifetime Value Simulator")
st.caption(
    "Interactive deployment demo for the selected Linear Regression model "
    "from the CRISP-DM Customer LTV portfolio project."
)

with st.container(border=True):
    st.subheader("Customer inputs")

    left, right = st.columns(2)

    with left:
        first_purchase_value = st.number_input(
            "First Purchase Value (R$)",
            min_value=0.0,
            value=708.0,
            step=10.0,
            format="%.2f",
        )
        recurring_label = st.selectbox(
            "Recurring First Purchase?",
            ["No", "Yes"],
        )
        entry_product = st.selectbox(
            "Entry Product",
            list(COEFFICIENTS["entry_product"].keys()),
        )
        sales_channel = st.selectbox(
            "Sales Channel",
            list(COEFFICIENTS["sales_channel"].keys()),
        )

    with right:
        gender = st.selectbox(
            "Gender",
            list(COEFFICIENTS["gender"].keys()),
        )
        education = st.selectbox(
            "Education",
            list(COEFFICIENTS["education"].keys()),
        )
        purchase_month = st.selectbox(
            "Purchase Month",
            list(range(1, 13)),
        )
        purchase_day = st.selectbox(
            "Purchase Day of Week",
            list(COEFFICIENTS["purchase_day_of_week"].keys()),
        )

prediction, contributions = predict_ltv(
    first_purchase_value=first_purchase_value,
    recurring=recurring_label == "Yes",
    entry_product=entry_product,
    sales_channel=sales_channel,
    gender=gender,
    education=education,
    purchase_month=purchase_month,
    purchase_day_of_week=purchase_day,
)

st.subheader("Predicted Customer Lifetime Value")

metric_col, r2_col, rmse_col, mae_col = st.columns(4)
metric_col.metric("Predicted LTV", brl(prediction))
r2_col.metric("Test R²", f"{TEST_R2:.4f}")
rmse_col.metric("Test RMSE", brl(TEST_RMSE))
mae_col.metric("Test MAE", brl(TEST_MAE))

st.info(
    "The model explains about 84.8% of the observed variation in LTV on the "
    "held-out test set. The estimate should be used as decision support, not "
    "as a guaranteed future customer value."
)

st.subheader("How the model arrived at this estimate")

rows = []
for factor, impact in contributions.items():
    if impact > 0:
        direction = "Increases"
    elif impact < 0:
        direction = "Decreases"
    else:
        direction = "Neutral"

    rows.append(
        {
            "Factor": factor,
            "Impact on LTV (R$)": round(impact, 2),
            "Direction": direction,
        }
    )

contribution_df = pd.DataFrame(rows)

table_col, chart_col = st.columns([1.1, 1])

with table_col:
    st.dataframe(
        contribution_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Impact on LTV (R$)": st.column_config.NumberColumn(
                format="R$ %.2f"
            )
        },
    )

with chart_col:
    chart_df = (
        contribution_df[contribution_df["Factor"] != "Model baseline"]
        .set_index("Factor")[["Impact on LTV (R$)"]]
    )
    st.bar_chart(chart_df)

with st.expander("Model interpretation and reference categories"):
    st.markdown(
        """
The prediction is the sum of a **model baseline** plus the contribution of
each selected customer characteristic.

Reference categories have a coefficient of zero:

- Entry product: **Commercial**
- Sales channel: **Checkout**
- Gender: **Female**
- Education: **Basic Education**
- Purchase month: **1**
- Purchase day of week: **Friday**

Positive contributions increase the predicted LTV relative to the reference
profile. Negative contributions reduce it.

These effects are **associations learned by the model**, not proof of causal
relationships.
"""
    )

st.divider()
st.caption(
    "Portfolio deployment demo · CRISP-DM · Linear Regression · "
    "Educational case study"
)
