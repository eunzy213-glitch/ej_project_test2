# pipeline/modeling.py
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

def train_linear_model(df):
    # 입력 X: SG (2차원 배열로 만들어야 sklearn이 인식합니다)
    X = df[["SG"]].values

    # 정답 y: BG (1차원 배열)
    y = df["BG"].values

    # 선형회귀 모델 생성
    model = LinearRegression()

    # 모델 학습
    model.fit(X, y)

    # 학습 데이터에 대한 예측값 생성
    y_pred = model.predict(X)

    # 성능 계산: R2
    r2 = r2_score(y, y_pred)

    # 성능 계산: RMSE
    # - 구버전 sklearn에서는 mean_squared_error에 squared 옵션이 없어서 직접 제곱근 처리합니다.
    rmse = mean_squared_error(y, y_pred) ** 0.5

    # 결과를 dict로 반환
    return {
        "r2": r2,
        "rmse": rmse
    }
