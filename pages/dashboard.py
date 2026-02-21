import streamlit as st

class Dashboard:
    def __init__(self, model_data):
        self.pipeline = model_data["pipeline"]
        self.threshold = model_data["threshold"]
        self.feature_names = model_data["feature_names"]
        self.metrics = model_data["metrics"]

    def _card(self, label, value):
        st.markdown(
            f"""
            <div style="
                background: #ffffff;
                border-radius: 10px;
                box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
                padding: 24px 28px;
                margin-bottom: 16px;
            ">
                <p style="
                    margin: 0;
                    font-size: 0.75rem;
                    font-weight: 600;
                    letter-spacing: 0.07em;
                    text-transform: uppercase;
                    color: #9CA3AF;
                ">{label}</p>
                <p style="
                    margin: 6px 0 0;
                    font-size: 1.8rem;
                    font-weight: 700;
                    color: #111827;
                    letter-spacing: -0.5px;
                ">{value}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render(self):
        st.markdown("# Customer Churn App for Banks")
        st.markdown("### Model Metrics Specification")

        recall    = self.metrics.get("recall", "N/A")
        precision = self.metrics.get("precision", "N/A")
        rocauc    = self.metrics.get("rocauc", self.metrics.get("roc_auc", "N/A"))

        recall_str    = f"{recall:.1%}"    if isinstance(recall,    (int, float)) else recall
        precision_str = f"{precision:.1%}" if isinstance(precision, (int, float)) else precision
        rocauc_str    = f"{rocauc:.3f}"    if isinstance(rocauc,    (int, float)) else rocauc
        threshold_str = f"{self.threshold:.2f}"

        col1, col2, col3, col4 = st.columns(4, gap="small")

        with col1:
            self._card("Recall", recall_str)
        with col2:
            self._card("Precision", precision_str)
        with col3:
            self._card("ROC-AUC", rocauc_str)
        with col4:
            self._card("Threshold", threshold_str)

        st.markdown("---")
        st.info("Pipeline loaded and ready for predictions")
