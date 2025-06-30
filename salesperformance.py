import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Performance Dashboard")

# Load dataset
df = pd.read_csv('sales_data_sample.csv', encoding='latin1')
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

# Sidebar filters
st.sidebar.header("Filter Data")
regions = st.sidebar.multiselect("Select Territory", options=df['TERRITORY'].dropna().unique())
products = st.sidebar.multiselect("Select Product Line", options=df['PRODUCTLINE'].unique())

# Apply filters
filtered_df = df.copy()
if regions:
    filtered_df = filtered_df[filtered_df['TERRITORY'].isin(regions)]
if products:
    filtered_df = filtered_df[filtered_df['PRODUCTLINE'].isin(products)]

# KPIs
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['SALES'].sum():,.2f}")
col2.metric("Avg Order Value", f"${filtered_df['SALES'].mean():,.2f}")
col3.metric("Unique Orders", f"{filtered_df['ORDERNUMBER'].nunique()}")

# Monthly sales trend
st.subheader("📈 Sales Over Time")
monthly_sales = filtered_df.groupby(pd.Grouper(key='ORDERDATE', freq='M'))['SALES'].sum().reset_index()
fig1, ax1 = plt.subplots()
sns.lineplot(data=monthly_sales, x='ORDERDATE', y='SALES', ax=ax1)
ax1.set_ylabel("Sales ($)")
ax1.set_title("Monthly Sales Trend")
st.pyplot(fig1)

# Product sales
st.subheader("🏆 Top Product Lines")
product_sales = filtered_df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False)
st.bar_chart(product_sales)

# Country sales
st.subheader("🌍 Sales by Country (Top 10)")
top_countries = (
    filtered_df.groupby('COUNTRY')['SALES']
    .sum().nlargest(10)
    .reset_index()
    .set_index('COUNTRY')
)
st.bar_chart(top_countries)

# Raw data
with st.expander("🔍 View Filtered Data"):
    st.dataframe(filtered_df)

# --- 📥 Export Options ---

st.subheader("📥 Download Filtered Data")

# CSV download
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv'
)

# Excel download
excel_buffer = BytesIO()
filtered_df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
excel_buffer.seek(0)

st.download_button(
    label="Download Excel",
    data=excel_buffer,
    file_name='filtered_sales_data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)