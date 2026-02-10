import joblib
import json

def load_churn_model():
    # Load pipeline
    model_data = joblib.load("models/churn_pipeline.pkl")

    # Load report
    with open("reports/churn_model_report.json", "r") as f:
        report_data = json.load(f)

    return {
        "pipeline": model_data["pipeline"],
        "threshold": model_data["threshold"],
        "feature_names": model_data["feature_names"],
        "metrics": model_data["metrics"],
        "threshold_analysis": report_data["threshold_analysis"],
        "business_impact": report_data["business_impact"],
        "confusion_matrix": report_data["confusion_matrix"]
    }
