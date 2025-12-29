# pipeline/metric_visualization.py
import os
import matplotlib.pyplot as plt
import pandas as pd


def plot_preprocessing_metrics(metric_records, save_dir):
    """
    전처리 방법별 R2, RMSE 시각화

    metric_records: list of dict
        [
          {"method": "01_range_filter", "r2": 0.42, "rmse": 18.3},
          ...
        ]
    """

    df = pd.DataFrame(metric_records)

    os.makedirs(save_dir, exist_ok=True)

    # -------------------------
    # 1. R2 Bar Plot
    # -------------------------
    plt.figure(figsize=(8, 5))
    plt.bar(df["method"], df["r2"])
    plt.ylabel("R-squared (↑)")
    plt.title("Model Performance by Preprocessing Method (R²)")
    plt.xticks(rotation=30, ha="right")

    for i, v in enumerate(df["r2"]):
        plt.text(i, v, f"{v:.3f}", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "preprocessing_r2.png"), dpi=300)
    plt.close()

    # -------------------------
    # 2. RMSE Bar Plot
    # -------------------------
    plt.figure(figsize=(8, 5))
    plt.bar(df["method"], df["rmse"])
    plt.ylabel("RMSE (mg/dL) (↓)")
    plt.title("Model Performance by Preprocessing Method (RMSE)")
    plt.xticks(rotation=30, ha="right")

    for i, v in enumerate(df["rmse"]):
        plt.text(i, v, f"{v:.1f}", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "preprocessing_rmse.png"), dpi=300)
    plt.close()
