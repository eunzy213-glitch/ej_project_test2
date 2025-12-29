# pipeline/analysis.py
import pandas as pd

def analyze_basic_stats(df, save_path):
    """기본 기술통계 저장"""
    df.describe().to_csv(f"{save_path}/descriptive_stats.csv")


def analyze_group_distribution(df, group_col, save_path):
    """특정 그룹 분포 분석"""
    if group_col not in df.columns or len(df) == 0:
        return

    df[group_col].value_counts(normalize=True)\
        .to_csv(f"{save_path}/{group_col}_distribution.csv")
