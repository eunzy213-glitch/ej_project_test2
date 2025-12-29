# pipeline/removed_analysis.py
import os
import pandas as pd
from scipy.stats import ttest_ind, ks_2samp


def analyze_removed_data(
    df_kept: pd.DataFrame,
    df_removed: pd.DataFrame,
    exp_dir: str,
    group_cols=None
):
    """
    제거된 데이터 분석
    1) 무엇이 제거되었는지 (기술통계)
    2) 누가 제거되었는지 (집단 분포)
    3) 진짜 이상치인지 (통계 검정)
    """

    os.makedirs(exp_dir, exist_ok=True)

    # ----------------------------------
    # 1. 무엇이 제거되었는지 (기술통계)
    # ----------------------------------
    df_removed.describe().to_csv(
        os.path.join(exp_dir, "removed_descriptive_stats.csv")
    )

    # ----------------------------------
    # 2. 누가 제거되었는지 (집단 분포)
    # ----------------------------------
    if group_cols is not None:
        for col in group_cols:
            if col in df_removed.columns:
                summary = pd.concat(
                    {
                        "Removed": df_removed[col].value_counts(normalize=True),
                        "Kept": df_kept[col].value_counts(normalize=True)
                    },
                    axis=1
                )
                summary.to_csv(
                    os.path.join(exp_dir, f"removed_vs_kept_{col}.csv")
                )

    # ----------------------------------
    # 3. 진짜 이상치인지? (통계 검정)
    # ----------------------------------
    stats_results = []

    for feature in ["SG", "BG"]:
        if feature not in df_removed.columns:
            continue

        # t-test (평균 차이)
        t_stat, t_p = ttest_ind(
            df_kept[feature],
            df_removed[feature],
            equal_var=False
        )

        # KS-test (분포 차이)
        ks_stat, ks_p = ks_2samp(
            df_kept[feature],
            df_removed[feature]
        )

        stats_results.append({
            "feature": feature,
            "t_statistic": t_stat,
            "t_p_value": t_p,
            "ks_statistic": ks_stat,
            "ks_p_value": ks_p
        })

    pd.DataFrame(stats_results).to_csv(
        os.path.join(exp_dir, "removed_statistical_tests.csv"),
        index=False
    )
