import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import mlflow
import mlflow.sklearn


def main():
    # 1) data
    df = pd.read_csv("data/housing.csv")
    X = df[["area"]]
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 2) model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 3) eval
    preds = model.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
    r2 = float(r2_score(y_test, preds))

    print(f"RMSE: {rmse:.4f} | R2: {r2:.4f}")

    # 4) mlflow tracking (local by default)
    # If you later run an MLflow server, set MLFLOW_TRACKING_URI env var.
    with mlflow.start_run() as run:
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("feature", "area")
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        # log model artifact to MLflow
        mlflow.sklearn.log_model(model, artifact_path="model")

    # 5) also save a local copy for FastAPI
    joblib.dump(model, "model.pkl")
    print("Saved model.pkl for serving.")

    # Optional: write a small inference log to demonstrate monitoring
    os.makedirs("logs", exist_ok=True)
    with open("logs/inference.log", "a") as f:
        f.write("TRAIN_COMPLETED\n")


if __name__ == "__main__":
    main()
