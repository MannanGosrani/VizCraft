import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import sweetviz as sv
import tempfile
import streamlit.components.v1 as components

st.set_page_config(page_title="CSV Data Analyzer", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: #ffffff;'>📊 VizCraft: CSV Data Analysis </h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the CSV
    df = pd.read_csv(uploaded_file)
    st.success("✅ CSV uploaded successfully!")

    # Extract column types
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📄 Overview", "📊 Visualizations", "🧠 Report"])

    # ==================== Tab 1: Overview ====================
    with tab1:
        st.markdown("### 🧾 Data Overview")

        with st.expander("📋 Show Raw Data"):
            st.dataframe(df.astype(str))

        with st.expander("🔍 Dataset Info"):
            st.markdown(f"- **Shape:** {df.shape}")
            st.markdown("#### Data Types")
            st.write(df.dtypes)
            st.markdown("#### Missing Values")
            st.write(df.isnull().sum())

        with st.expander("📈 Summary Statistics"):
            st.write(df.describe())

    # ==================== Tab 2: Visualizations ====================
    with tab2:
        st.markdown("### 📊 Explore Your Data")

        # Numeric Visualization
        if numeric_cols:
            with st.expander("📈 Visualize Numeric Column"):
                selected_num = st.selectbox("Choose a numeric column", numeric_cols, key="num_col")
                chart_type_num = st.radio("Select chart type", ["Histogram", "Line Chart"], horizontal=True, key="num_type")

                if chart_type_num == "Histogram":
                    fig = px.histogram(df, x=selected_num, nbins=30, title=f"Histogram of {selected_num}", text_auto=True)
                    fig.update_traces(marker_line_color="black", marker_line_width=1.5)
                    fig.update_layout(bargap=0.1, xaxis_title=selected_num, yaxis_title="Count")
                    st.plotly_chart(fig, use_container_width=True)
                elif chart_type_num == "Line Chart":
                    fig = px.line(df, y=selected_num, title=f"Line Chart of {selected_num}")
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available for visualization.")

        # Categorical Visualization
        if cat_cols:
            with st.expander("📈 Visualize Categorical Column"):
                        selected_cat = st.selectbox("Choose a categorical column", cat_cols, key="cat_col")
                        chart_type_cat = st.radio("Select chart type", ["Count Plot", "Pie Chart"], horizontal=True, key="cat_type")
                        
                        if chart_type_cat == "Count Plot":
                            fig2 = px.histogram(df, x=selected_cat, color=selected_cat, title=f"Count Plot of {selected_cat}")
                            st.plotly_chart(fig2, use_container_width=True)
                        elif chart_type_cat == "Pie Chart":
                            pie_df = df[selected_cat].value_counts().reset_index()
                            pie_df.columns = [selected_cat, 'Count']
                            fig2 = px.pie(pie_df, names=selected_cat, values='Count', title=f"Pie Chart of {selected_cat}")
                            st.plotly_chart(fig2, use_container_width=True)
                        else:
                            st.info("No categorical columns available for visualization.")
                    
        # Correlation Analysis 
        if numeric_cols:
            st.markdown("### 🧠 Correlation Analysis")

            with st.expander("📌 Show Correlation Heatmap"):
                st.markdown("Visualize relationships between numeric features.")
                corr = df[numeric_cols].corr()
                fig_corr, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
                st.pyplot(fig_corr)
                plt.clf()  # Clear the figure to avoid overlap in reruns

            with st.expander("🔍 Show Pairplot (for smaller datasets only)"):
                if df.shape[0] <= 200:
                    st.markdown("Visualizes variable relationships via scatter matrix.")
                    pairplot_fig = sns.pairplot(df[numeric_cols])
                    st.pyplot(pairplot_fig)
                    plt.clf()
                else:
                    st.info("Dataset too large for pairplot (limit: 200 rows).")
        
        # Outlier Detection 
        if numeric_cols:
            st.markdown("### 🧪 Outlier Detection")

            with st.expander("📦 Detect Outliers (Boxplot + IQR)"):
                selected_outlier_col = st.selectbox("Select a column for outlier detection", numeric_cols, key="outlier_col")

                # Calculate IQR
                Q1 = df[selected_outlier_col].quantile(0.25)
                Q3 = df[selected_outlier_col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                # Flag outliers
                outliers = df[(df[selected_outlier_col] < lower_bound) | (df[selected_outlier_col] > upper_bound)]
                num_outliers = outliers.shape[0]

                # Show outlier summary
                st.markdown(f"- **Total Outliers:** `{num_outliers}`")
                st.markdown(f"- **Lower Bound:** `{lower_bound:.2f}`")
                st.markdown(f"- **Upper Bound:** `{upper_bound:.2f}`")

                # Show boxplot
                fig_box, ax = plt.subplots(figsize=(8, 1.5))
                sns.boxplot(x=df[selected_outlier_col], ax=ax, color="#00bfc4")
                ax.set_title(f"Boxplot of {selected_outlier_col}")
                st.pyplot(fig_box)
                plt.clf()

        # Missing Value Imputation 
        st.markdown("### 🧼 Handle Missing Values")

        with st.expander("🧰 Fill or Drop Missing Values"):
            # Check for any missing values
            missing_cols = df.columns[df.isnull().any()].tolist()

            if missing_cols:
                selected_missing_col = st.selectbox("Select a column with missing values", missing_cols, key="miss_col")
                st.markdown(f"- **Missing count:** `{df[selected_missing_col].isnull().sum()}`")
                col_dtype = df[selected_missing_col].dtype

                if pd.api.types.is_numeric_dtype(df[selected_missing_col]):
                    impute_option = st.radio("Choose a strategy", ["Mean", "Median", "Drop Rows", "Drop Column"], horizontal=True, key="num_impute")
                else:
                    impute_option = st.radio("Choose a strategy", ["Mode", "Drop Rows", "Drop Column"], horizontal=True, key="cat_impute")

                if st.button("🛠️ Apply Imputation"):
                    if impute_option == "Mean":
                        value = df[selected_missing_col].mean()
                        df[selected_missing_col].fillna(value, inplace=True)
                        st.success(f"Filled missing values in '{selected_missing_col}' with mean: {value:.2f}")
                    elif impute_option == "Median":
                        value = df[selected_missing_col].median()
                        df[selected_missing_col].fillna(value, inplace=True)
                        st.success(f"Filled missing values in '{selected_missing_col}' with median: {value:.2f}")
                    elif impute_option == "Mode":
                        value = df[selected_missing_col].mode().iloc[0]
                        df[selected_missing_col].fillna(value, inplace=True)
                        st.success(f"Filled missing values in '{selected_missing_col}' with mode: {value}")
                    elif impute_option == "Drop Rows":
                        before = df.shape[0]
                        df.dropna(subset=[selected_missing_col], inplace=True)
                        after = df.shape[0]
                        st.success(f"Dropped {before - after} rows with missing values in '{selected_missing_col}'")
                    elif impute_option == "Drop Column":
                        df.drop(columns=[selected_missing_col], inplace=True)
                        st.success(f"Dropped column '{selected_missing_col}' from dataset.")

                    # Show updated info
                    st.write("✅ Updated DataFrame Preview:")
                    st.dataframe(df.head())
            else:
                st.info("🎉 No missing values detected in your dataset.")

        # Pivot Table Style Aggregation
        st.markdown("### 📊 Grouped Aggregation (Pivot Table Style)")

        with st.expander("🧮 Group & Summarize Data"):
            if cat_cols and numeric_cols:
                group_col = st.selectbox("Select a column to group by (categorical)", cat_cols, key="groupby_col")
                agg_cols = st.multiselect("Select numeric column(s) to aggregate", numeric_cols, key="agg_cols")

                if agg_cols:
                    agg_func = st.selectbox("Choose aggregation function", ["sum", "mean", "median", "count", "min", "max"], key="agg_func")

                    if st.button("Generate Grouped Summary"):
                        try:
                            agg_df = df.groupby(group_col)[agg_cols].agg(agg_func).reset_index()
                            st.success(f"Showing {agg_func} of selected columns grouped by '{group_col}'")
                            st.dataframe(agg_df)
                        except Exception as e:
                            st.error(f"Error generating summary: {e}")
                else:
                    st.info("Please select at least one numeric column to aggregate.")
            else:
                st.info("Dataset must contain at least one categorical and one numeric column.")

        
    # ==================== Tab 3: Report ====================
    with tab3:
        st.markdown("### 🧠 Generate Data Profiling Report")
        if st.button("Generate Sweetviz Report"):
            with st.spinner("Generating Sweetviz report..."):
                report = sv.analyze(df)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
                    report.show_html(tmpfile.name, open_browser=False)
                    st.success("✅ Report generated below ⬇️")
                    with open(tmpfile.name, 'r', encoding='utf-8') as f:
                        html = f.read()
                        components.html(html, height=1000, scrolling=True)

    # Footer
    st.markdown("---")
    st.markdown("Made by Mannan Gosrani • © 2025")

else:
    st.warning("📂 Please upload a CSV file to begin.")
