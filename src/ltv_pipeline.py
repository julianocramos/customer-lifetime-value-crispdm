"""Customer Lifetime Value modeling pipeline.

The original educational dataset is not included in this repository.
The source dataset uses Portuguese field names and categories, so this module
translates the source schema into English before preprocessing and modeling.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler

TARGET = "LTV"

NUMERIC_FEATURES = ["first_purchase_value"]
BINARY_FEATURES = ["recurring_first_purchase"]
CATEGORICAL_FEATURES = [
    "entry_product",
    "sales_channel",
    "gender",
    "education",
    "purchase_month",
    "purchase_day_of_week",
]

SOURCE_COLUMN_MAP = {
    "valor_1_compra": "first_purchase_value",
    "recorrente_1_compra": "recurring_first_purchase",
    "Produto Fonte": "entry_product",
    "Fonte Campanha": "sales_channel",
    "Sexo": "gender",
    "Formacao": "education",
    "mes_compra": "purchase_month",
    "dia_semana_compra": "purchase_day_of_week",
}

PRODUCT_MAP = {
    "Análise de Dados": "Data Analysis",
    "Ciência de Dados": "Data Science",
    "Comercial": "Commercial",
    "Comunidade": "Community",
    "Excel": "Excel",
    "Full Stack Javascript": "Full Stack JavaScript",
    "Outros": "Other",
    "Power BI": "Power BI",
    "Python": "Python",
    "Vitalício": "Lifetime Access",
}

SALES_CHANNEL_MAP = {
    "Checkout": "Checkout",
    "Comercial": "Commercial",
    "Lançamento": "Launch",
    "Lista Espera": "Waitlist",
    "Outros": "Other",
    "Tráfego Direto": "Direct Traffic",
    "Webinar": "Webinar",
}

GENDER_MAP = {
    "Feminino": "Female",
    "Masculino": "Male",
    "Outros": "Other",
}

EDUCATION_MAP = {
    "Fundamental": "Basic Education",
    "Médio": "High School",
    "Não Informado": "Not Reported",
    "Superior Completo": "Higher Education - Complete",
    "Superior Incompleto": "Higher Education - Incomplete",
    "Superior+": "Higher Education+",
}

DAY_OF_WEEK_MAP = {
    "Domingo": "Sunday",
    "Segunda-feira": "Monday",
    "Terça-feira": "Tuesday",
    "Quarta-feira": "Wednesday",
    "Quinta-feira": "Thursday",
    "Sexta-feira": "Friday",
    "Sábado": "Saturday",
}


def translate_source_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Translate the prepared source dataset into the English modeling schema."""
    translated = df.rename(columns=SOURCE_COLUMN_MAP).copy()

    translated["entry_product"] = translated["entry_product"].replace(PRODUCT_MAP)
    translated["sales_channel"] = translated["sales_channel"].replace(SALES_CHANNEL_MAP)
    translated["gender"] = translated["gender"].replace(GENDER_MAP)
    translated["education"] = translated["education"].replace(EDUCATION_MAP)
    translated["purchase_day_of_week"] = translated["purchase_day_of_week"].replace(
        DAY_OF_WEEK_MAP
    )

    return translated


def build_preprocessor() -> ColumnTransformer:
    """Create the preprocessing block used by every regression model."""
    numeric_transformer = Pipeline(
        steps=[("scaler", StandardScaler())]
    )

    categorical_transformer = Pipeline(
        steps=[
            (
                "onehot",
                OneHotEncoder(
                    drop="first",
                    handle_unknown="ignore",
                ),
            )
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, NUMERIC_FEATURES),
            ("categorical", categorical_transformer, CATEGORICAL_FEATURES),
            ("binary", "passthrough", BINARY_FEATURES),
        ]
    )


def split_data(df: pd.DataFrame):
    """Split the dataset into 80% training and 20% test sets."""
    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )


def build_models() -> dict[str, Pipeline]:
    """Return the four regression approaches compared in the project."""
    return {
        "Dummy": Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("regressor", DummyRegressor(strategy="mean")),
            ]
        ),
        "Linear": Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("regressor", LinearRegression()),
            ]
        ),
        "Poly (d=2)": Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                (
                    "polynomial_features",
                    PolynomialFeatures(
                        degree=2,
                        include_bias=False,
                    ),
                ),
                ("regressor", LinearRegression()),
            ]
        ),
        "RF": Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                (
                    "regressor",
                    RandomForestRegressor(
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
    }


def cross_validate_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> pd.DataFrame:
    """Run 5-fold cross-validation on the training set using R²."""
    kfold = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    rows = []

    for model_name, model in build_models().items():
        scores = cross_val_score(
            model,
            X_train,
            y_train,
            cv=kfold,
            scoring="r2",
            n_jobs=1,
        )

        row = {
            "model": model_name,
            **{
                f"fold_{index + 1}": score
                for index, score in enumerate(scores)
            },
            "mean_r2": scores.mean(),
        }
        rows.append(row)

    return pd.DataFrame(rows)


def evaluate_model(
    model: Pipeline,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> dict[str, float]:
    """Fit a model and evaluate it on the held-out test set."""
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    return {
        "r2": r2_score(y_test, predictions),
        "rmse": float(
            np.sqrt(
                mean_squared_error(
                    y_test,
                    predictions,
                )
            )
        ),
        "mae": float(
            mean_absolute_error(
                y_test,
                predictions,
            )
        ),
    }


def build_final_model() -> Pipeline:
    """Build the selected production-style model."""
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("regressor", LinearRegression()),
        ]
    )


if __name__ == "__main__":
    raw_data = pd.read_csv(
        "data/ltv_base_tratada_cardinalidade_final.csv"
    )
    data = translate_source_schema(raw_data)

    X_train, X_test, y_train, y_test = split_data(data)

    cv_results = cross_validate_models(
        X_train,
        y_train,
    )
    print(cv_results.to_string(index=False))

    final_model = build_final_model()
    metrics = evaluate_model(
        final_model,
        X_train,
        X_test,
        y_train,
        y_test,
    )

    print("\nLinear Regression test metrics:")
    print(metrics)
