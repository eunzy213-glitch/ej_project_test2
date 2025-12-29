# pipeline/removed_visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_removed_vs_kept_bar(csv_path, save_path, title):
    """
    removed_vs_kept_*.csv 파일을 읽어서
    제거(Removed) vs 유지(Kept) 비율을 막대그래프로 시각화
    """

    # CSV 로드
    df = pd.read_csv(csv_path, index_col=0)

    # 막대그래프 생성
    df.plot(
        kind="bar",
        figsize=(7, 5)
    )

    plt.title(title)
    plt.ylabel("Ratio")
    plt.xlabel("")
    plt.ylim(0, 1)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # 이미지 저장
    plt.savefig(save_path, dpi=300)
    plt.close()


def plot_all_removed_vs_kept(exp_dir):
    """
    전처리 실험 폴더(exp_dir) 안에 있는
    모든 removed_vs_kept_*.csv 파일을 자동으로 찾아
    각각 막대그래프로 저장
    """

    for file in os.listdir(exp_dir):
        if file.startswith("removed_vs_kept_") and file.endswith(".csv"):
            var_name = file.replace("removed_vs_kept_", "").replace(".csv", "")

            csv_path = os.path.join(exp_dir, file)
            save_path = os.path.join(
                exp_dir,
                f"plot_removed_vs_kept_{var_name}.png"
            )

            plot_removed_vs_kept_bar(
                csv_path=csv_path,
                save_path=save_path,
                title=f"Removed vs Kept by {var_name}"
            )
