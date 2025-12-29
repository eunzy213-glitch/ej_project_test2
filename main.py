# main.py
import pandas as pd
import os

from pipeline.pipeline import run_pipeline
from pipeline.preprocessing import (
    range_filter,
    residual_filter,
    isolation_forest_filter
)


def main():
    print("=== Project Pipeline Start ===")

    # Raw 데이터 로드
    data_path = "data/dataset_update.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"데이터 파일이 없습니다: {data_path}")

    df_raw = pd.read_csv(data_path)
    print(f"[INFO] Raw data loaded: {df_raw.shape}")

    # 전처리 실험 정의
    preprocessing_methods = {
        "01_range_filter": range_filter,
        "02_residual_filter": residual_filter,
        "03_isolation_forest": isolation_forest_filter
    }

    # 파이프라인 실행
    run_pipeline(
        df_raw=df_raw,
        preprocessing_methods=preprocessing_methods,
        result_root="results"
    )

    print("=== Project Pipeline Finished ===")


if __name__ == "__main__":
    main()
