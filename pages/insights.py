import streamlit as st
import pandas as pd


class Insights:
    def __init__(self, model_data):
        self.threshold_data = model_data["threshold_analysis"]

    def render(self):
        st.markdown("# Business Insights & Threshold Optimization")

        # Business assumptions
        st.markdown("## Business Assumptions")

        col1, col2 = st.columns(2)
        with col1:
            promotion_cost = st.number_input(
                "Cost per promotion ($)",
                value=200,
                step=50
            )
        with col2:
            customer_value = st.number_input(
                "Value of saving a churned customer ($)",
                value=1000,
                step=100
            )

        # Load threshold dataframe
        df = pd.DataFrame(self.threshold_data)

        # Recalculate net value dynamically
        df["net_value"] = (
            (df["predicted_churners"] - df["fp_count"]) * customer_value
            - df["fp_count"] * promotion_cost
        )

        # Best threshold
        best_row = df.loc[df["net_value"].idxmax()]

        st.divider()
        st.markdown("## Recommended Threshold")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Best Threshold", best_row["threshold"])
        c2.metric("Net Value", f"${int(best_row['net_value']):,}")
        c3.metric("Recall", f"{best_row['recall']:.2f}")
        c4.metric("False Positives", int(best_row["fp_count"]))

        st.success(
            f"Threshold **{best_row['threshold']}** maximizes business value under current assumptions."
        )

        st.divider()
        st.markdown("## Threshold Impact Table")

        st.dataframe(
            df.sort_values("threshold"),
            use_container_width=True
        )

        st.divider()
        st.markdown("## Business Interpretation")

        st.markdown(
            f"""
            - Lower thresholds prioritize recall but increase campaign cost  
            - Higher thresholds reduce cost but miss churners  
            - **Threshold {best_row['threshold']}** provides the optimal financial trade-off
            """
        )
