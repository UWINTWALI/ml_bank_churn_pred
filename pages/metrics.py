import streamlit as st

class Metrics:
    def __init__(self, model_data):
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
        st.markdown("## Model Performance")

        recall    = self.metrics.get("recall", "N/A")
        precision = self.metrics.get("precision", "N/A")
        f1        = self.metrics.get("f1", "N/A")
        rocauc    = self.metrics.get("rocauc", self.metrics.get("roc_auc", "N/A"))
        threshold = self.metrics.get("threshold", "N/A")

        recall_str    = f"{recall:.1%}"    if isinstance(recall,    (int, float)) else recall
        precision_str = f"{precision:.1%}" if isinstance(precision, (int, float)) else precision
        f1_str        = f"{f1:.3f}"        if isinstance(f1,        (int, float)) else f1
        rocauc_str    = f"{rocauc:.3f}"    if isinstance(rocauc,    (int, float)) else rocauc
        threshold_str = f"{threshold:.2f}" if isinstance(threshold, (int, float)) else threshold

        col1, col2 = st.columns(2, gap="large")

        with col1:
            self._card("Recall",    recall_str)
            self._card("Precision", precision_str)
            self._card("F1-Score",  f1_str)

        with col2:
            self._card("ROC-AUC",   rocauc_str)
            self._card("Threshold", threshold_str)

        st.markdown("<br>", unsafe_allow_html=True)
        st.success("Pipeline loaded — Ready for predictions")
