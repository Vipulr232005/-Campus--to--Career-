"""
Stub: Train dropout risk model (scikit-learn).
Run with synthetic or real data, then save model to ML_RISK_MODEL_PATH.
Example: python -m ml_risk_engine.train_stub
"""
import os
import joblib
import numpy as np
from pathlib import Path

# Feature order: attendance_pct, avg_grade_point, assignment_submission_rate, avg_assignment_marks, cgpa
FEATURE_NAMES = ["attendance_pct", "avg_grade_point", "assignment_submission_rate", "avg_assignment_marks", "cgpa"]


def get_synthetic_data(n=200):
    """Generate synthetic data for demo. Replace with real DB export."""
    np.random.seed(42)
    X = np.column_stack([
        np.clip(np.random.beta(8, 2, n) * 100, 0, 100),   # attendance
        np.clip(np.random.beta(5, 2, n) * 10, 0, 10),     # grade
        np.clip(np.random.beta(8, 2, n) * 100, 0, 100),   # submission
        np.clip(np.random.beta(5, 2, n) * 100, 0, 100),   # assign marks
        np.clip(np.random.beta(5, 2, n) * 10, 0, 10),     # cgpa
    ])
    # Simple target: high risk if any metric is low
    y = (X[:, 0] < 70).astype(int) * 0.5 + (X[:, 1] < 5).astype(int) * 0.3 + (X[:, 2] < 70).astype(int) * 0.2
    y = np.clip(y + np.random.randn(n) * 0.1, 0, 1)
    return X, y


def train_and_save():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

    X, y = get_synthetic_data()
    y_bin = (y >= 0.5).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y_bin, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"Train accuracy: {model.score(X_train, y_train):.3f}, Test accuracy: {acc:.3f}")

    out_dir = Path(__file__).resolve().parent / "models"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "dropout_model.pkl"
    joblib.dump(model, out_path)
    print(f"Model saved to {out_path}")
    return out_path


if __name__ == "__main__":
    train_and_save()
