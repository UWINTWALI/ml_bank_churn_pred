import streamlit as st

class Dashboard:
    def __init__(self, model_data):
        self.pipeline = model_data["pipeline"]
        self.threshold = model_data["threshold"]
        self.feature_names = model_data["feature_names"]
        self.metrics = model_data["metrics"]
    
    def render(self):
        st.markdown("# Customer Churn App for Banks")
        st.markdown("### Model Metrics Specification")

        
        # Score cards for metrics
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            recall = self.metrics.get('recall', 'N/A')
            recall_str = f"{recall:.1%}" if isinstance(recall, (int, float)) else recall
            st.metric("Recall", recall_str)
        with col2:
            precision = self.metrics.get('precision', 'N/A')
            precision_str = f"{precision:.1%}" if isinstance(precision, (int, float)) else precision
            st.metric("Precision", precision_str)
        with col3:
            rocauc = self.metrics.get('rocauc', self.metrics.get('roc_auc', 'N/A'))
            rocauc_str = f"{rocauc:.3f}" if isinstance(rocauc, (int, float)) else rocauc
            st.metric("ROC-AUC", rocauc_str)
        with col4:
            st.metric("Threshold", f"{self.threshold:.2f}")

        st.markdown("---")
        st.info("**Pipeline loaded and ready for predictions**")
