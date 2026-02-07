import streamlit as st

class Metrics:
    def __init__(self, model_data):
        self.metrics = model_data[3]
    
    def render(self):
        st.markdown("# Model Performance")
        
        col1, col2 = st.columns(2)
        with col1:
            recall = self.metrics.get('recall', 'N/A')
            recall_str = f"{recall:.1%}" if isinstance(recall, (int, float)) else recall
            st.metric("Recall", recall_str)
            
            precision = self.metrics.get('precision', 'N/A')
            precision_str = f"{precision:.1%}" if isinstance(precision, (int, float)) else precision
            st.metric("Precision", precision_str)
            
            f1 = self.metrics.get('f1', 'N/A')
            f1_str = f"{f1:.3f}" if isinstance(f1, (int, float)) else f1
            st.metric("F1-Score", f1_str)
        with col2:
            rocauc = self.metrics.get('rocauc', self.metrics.get('roc_auc', 'N/A'))
            rocauc_str = f"{rocauc:.3f}" if isinstance(rocauc, (int, float)) else rocauc
            st.metric("ROC-AUC", rocauc_str)
            
            threshold = self.metrics.get('threshold', 'N/A')
            threshold_str = f"{threshold:.2f}" if isinstance(threshold, (int, float)) else threshold
            st.metric("Threshold", threshold_str)
        
        st.success("Pipeline loaded: Ready for predictions")
