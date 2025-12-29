# pipeline/pipeline.py
import os

from pipeline.visualization import plot_removed_vs_kept
from pipeline.modeling import train_linear_model
from pipeline.removed_analysis import analyze_removed_data
from pipeline.metric_visualization import plot_preprocessing_metrics
from pipeline.removed_visualization import plot_all_removed_vs_kept


def run_pipeline(df_raw, preprocessing_methods: dict, result_root="results"):

    os.makedirs(result_root, exist_ok=True)
    total_n = len(df_raw)

    # ⭐ 전처리별 성능 기록용
    metric_records = []

    for name, method_fn in preprocessing_methods.items():
        print(f"\n[Preprocessing Experiment] {name}")

        exp_dir = os.path.join(result_root, name)
        os.makedirs(exp_dir, exist_ok=True)

        df_raw_tmp = df_raw.copy()
        df_raw_tmp["_row_id"] = df_raw_tmp.index

        # 전처리
        df_cleaned = method_fn(df_raw_tmp.copy())
        df_cleaned["_row_id"] = df_cleaned.index

        # 제거 데이터
        df_removed = df_raw_tmp[
            ~df_raw_tmp["_row_id"].isin(df_cleaned["_row_id"])
        ].drop(columns="_row_id")

        df_cleaned = df_cleaned.drop(columns="_row_id")

        # 제거율
        n_before = total_n
        n_after = len(df_cleaned)
        n_removed = n_before - n_after
        removed_ratio = (n_removed / n_before) * 100

        print(f" - Total samples     : {n_before}")
        print(f" - Remaining samples : {n_after}")
        print(f" - Removed samples   : {n_removed} ({removed_ratio:.1f}%)")

        # 제거 데이터 분석
        analyze_removed_data(
            df_kept=df_cleaned,
            df_removed=df_removed,
            exp_dir=exp_dir,
            group_cols=["Meal_Status", "BMI_Class", "Age_Group", "Exercise", "Family_History", "Pregnancy"]
        )

        # ⭐ 여기 추가 ⭐
        # 변수별 제거 vs 유지 비율 막대그래프 자동 생성
        plot_all_removed_vs_kept(exp_dir)
        
        # -------------------------
        # ⭐ 모델 성능 계산
        # -------------------------
        metrics = train_linear_model(df_cleaned)

        metric_records.append({
            "method": name,
            "r2": metrics["r2"],
            "rmse": metrics["rmse"]
        })

        with open(os.path.join(exp_dir, "model_metrics.txt"), "w") as f:
            f.write(str(metrics))

        # 시각화
        plot_removed_vs_kept(df_cleaned, df_removed, exp_dir)

    # -------------------------
    # ⭐ 전처리별 성능 시각화 (마지막에 한 번)
    # -------------------------
    plot_preprocessing_metrics(
        metric_records=metric_records,
        save_dir=result_root
    )
