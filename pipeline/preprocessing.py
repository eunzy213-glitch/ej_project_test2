# pipeline/preprocessing.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression


def range_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    [실험 1] 단순 범위 기반 필터링
    """
    return df[(df["BG"] >= 70) & (df["BG"] <= 140)].copy()


def residual_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    [실험 2] 잔차 기반 이상치 제거
    """
    X = df[["SG"]].values
    y = df["BG"].values

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    residuals = np.abs(y - y_pred)
    threshold = residuals.mean() + 1.5 * residuals.std()

    return df[residuals < threshold].copy()


def isolation_forest_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    [실험 3] Isolation Forest 기반 이상치 제거
    """
    X = df[["SG", "BG"]].values

    iso = IsolationForest(
        contamination=0.05,
        random_state=42
    )
    mask = iso.fit_predict(X) == 1

    return df[mask].copy()
