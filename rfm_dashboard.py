import pandas as pd
import datetime as dt
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# Load data
file_path = 'rfm_data.csv'  # Change this to the actual path if necessary
data = pd.read_csv(file_path)

# Convert PurchaseDate to datetime
data['PurchaseDate'] = pd.to_datetime(data['PurchaseDate'])

# Define reference date for recency calculation
reference_date = dt.datetime(2023, 7, 1)

# Calculate RFM metrics
rfm = data.groupby('CustomerID').agg({
    'PurchaseDate': lambda x: (reference_date - x.max()).days,
    'OrderID': 'count',
    'TransactionAmount': 'sum'
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# Filter out non-positive monetary values
rfm = rfm[rfm['Monetary'] > 0]

# Define RFM score thresholds
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, ['1', '2', '3', '4'])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, ['4', '3', '2', '1'])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, ['4', '3', '2', '1'])

# Concatenate RFM score to a single RFM segment
rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1).astype(int)

# Define RFM segments
def rfm_segment(df):
    if df['RFM_Score'] >= 9:
        return 'Champions'
    elif df['RFM_Score'] >= 8:
        return 'Loyal Customers'
    elif df['RFM_Score'] >= 7:
        return 'Potential Loyalists'
    elif df['RFM_Score'] >= 6:
        return 'Recent Customers'
    elif df['RFM_Score'] >= 5:
        return 'Promising'
    elif df['RFM_Score'] >= 4:
        return 'Need Attention'
    elif df['RFM_Score'] >= 3:
        return 'At Risk'
    else:
        return 'Lost'

rfm['RFM_Segment'] = rfm.apply(rfm_segment, axis=1)

# Count of customers in each segment
segment_counts = rfm['RFM_Segment'].value_counts().reset_index()
segment_counts.columns = ['RFM_Segment', 'Count']

# Streamlit Dashboard
st.set_page_config(page_title="RFM Analysis Dashboard", page_icon=":bar_chart:", layout="wide")

# Add custom CSS with animations
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .stApp {
        background-image: url('https://wallpapers.com/images/high/white-color-background-ghw6e685ri75chj4.webp');
        background-size: cover;
        animation: fadeIn 2s ease-in;
    }

    .header {
        text-align: center;
    }

    .header h1 {
        font-size: 3em;
        color: #4b0082;
        animation: fadeIn 3s ease-in;
    }

    .header img {
        margin-top: -20px;
        width: 60px;
        animation: fadeIn 3s ease-in;
    }

    .segment {
        margin: 20px 0;
        text-align: center;
        color: purple;
        animation: fadeIn 3s ease-in;
    }

    .segment h3 {
        color: purple;
    }

    .segment p {
        color: purple;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        animation: fadeIn 2s ease-in;
    }

    .metric {
        text-align: center;
        background: #fff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        width: 200px;
        color: purple;
        animation: fadeIn 2s ease-in;
    }

    .metric h3 {
        color: #4b0082;
    }

    .metric p {
        font-size: 2em;
        color: black;
        margin: 0;
    }

    .plot-container {
        animation: fadeIn 3s ease-in;
    }

    .stButton>button {
        color: white !important; /* Ensure text color is always white */
        background: purple;
        width: 900px;
        padding: 10px 20px;
        border: 2px solid purple;
        border-radius: 5px;
        font-size: 1.5em;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-left: 110px;
    }
    .center-button {
        display: flex;
        justify-content: center;
    }

    .stButton>button:hover {
        background-color: darkturquoise;
    }

    .stButton>button:active {
        background-color: darkturquoise;
    }

    .stSelectbox label {
        color: purple !important;
    }

    .stSelectbox select {
        color: purple !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='header'>
    <h1>RFM Analysis Dashboard</h1>
    <img src='https://img.icons8.com/fluency/48/000000/customer-insight.png'/>
    <p style="color:purple">Analyze your customer segments based on Recency, Frequency, and Monetary values</p>
</div>
""", unsafe_allow_html=True)

# Data Preview Button with Toggle
if 'data_preview' not in st.session_state:
    st.session_state.data_preview = False

if st.button('Data Preview'):
    st.session_state.data_preview = not st.session_state.data_preview

if st.session_state.data_preview:
    st.markdown("<div class='center-button'>", unsafe_allow_html=True)
    st.dataframe(data, width=900)
    st.markdown("</div>", unsafe_allow_html=True)

# Metrics
total_customers = rfm['CustomerID'].nunique()
avg_recency = int(rfm['Recency'].mean())
avg_frequency = int(rfm['Frequency'].mean())
avg_monetary = int(rfm['Monetary'].mean())

st.markdown(f"""
<div class='metric-container'>
    <div class='metric'>
        <h3>Total Customers</h3>
        <p>{total_customers}</p>
    </div>
    <div class='metric'>
        <h3>Average Recency</h3>
        <p>{avg_recency}</p>
    </div>
    <div class='metric'>
        <h3>Average Frequency</h3>
        <p>{avg_frequency}</p>
    </div>
    <div class='metric'>
        <h3>Average Monetary Value</h3>
        <p>{avg_monetary}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Dropdown for analysis type
st.sidebar.title("Analysis Options")
analysis_type = st.sidebar.selectbox("Analyze customer segments based on RFM scores:", [
    "Comparison of RFM Segments",
    "RFM Value Segment Distribution",
    "Distribution of RFM Values within Customer Segment",
    "Correlation Matrix of RFM Values within Champions Segment"
])

# Plot based on selection
if analysis_type == "Comparison of RFM Segments":
    st.markdown("""
        <div class='segment'>
            <h3>Comparison of RFM Segments</h3>
            <p>See how many customers fall into each RFM segment.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Bar chart of segment counts
    fig_bar = px.bar(segment_counts, x='RFM_Segment', y='Count', title='Count of Customers in Each RFM Segment', color='RFM_Segment')
    st.plotly_chart(fig_bar)

    # Pie chart of percentage distribution
    fig_pie = px.pie(segment_counts, values='Count', names='RFM_Segment', title='Percentage Distribution of Customers by RFM Segment')
    st.plotly_chart(fig_pie)

    # Histogram of RFM Scores
    fig_hist = px.histogram(rfm, x='RFM_Score', title='RFM Score Distribution', nbins=10, color='RFM_Score')
    st.plotly_chart(fig_hist)

    # Scatter plot example
    fig_scatter = px.scatter(rfm, x='Recency', y='Monetary', color='RFM_Segment', title='Recency vs Monetary Value')
    st.plotly_chart(fig_scatter)

elif analysis_type == "RFM Value Segment Distribution":
    st.markdown("""
        <div class='segment'>
            <h3>RFM Value Segment Distribution</h3>
            <p>Explore the distribution of RFM values within customer segments.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Histogram of Recency
    fig_hist_recency = px.histogram(rfm, x='Recency', title='Distribution of Recency Values', nbins=20, color='RFM_Segment')
    st.plotly_chart(fig_hist_recency)

    # Histogram of Frequency
    fig_hist_frequency = px.histogram(rfm, x='Frequency', title='Distribution of Frequency Values', nbins=20, color='RFM_Segment')
    st.plotly_chart(fig_hist_frequency)

    # Histogram of Monetary
    fig_hist_monetary = px.histogram(rfm, x='Monetary', title='Distribution of Monetary Values', nbins=20, color='RFM_Segment')
    st.plotly_chart(fig_hist_monetary)

    # Box plot of RFM Values by Segment
    fig_box_rfm = px.box(rfm, x='RFM_Segment', y='Recency', title='Recency Values by Segment', color='RFM_Segment')
    st.plotly_chart(fig_box_rfm)

elif analysis_type == "Distribution of RFM Values within Customer Segment":
    st.markdown("""
        <div class='segment'>
            <h3>Distribution of RFM Values within Customer Segment</h3>
            <p>Analyze the distribution of RFM values within a specific customer segment.</p>
        </div>
    """, unsafe_allow_html=True)
    
    segment = st.sidebar.selectbox("Select Customer Segment", rfm['RFM_Segment'].unique())

    segment_data = rfm[rfm['RFM_Segment'] == segment]
    
    # Histogram of Recency for the selected segment
    fig_hist_segment_recency = px.histogram(segment_data, x='Recency', title=f'Recency Values Distribution in {segment} Segment', nbins=20, color='RFM_Segment')
    st.plotly_chart(fig_hist_segment_recency)

    # Histogram of Frequency for the selected segment
    fig_hist_segment_frequency = px.histogram(segment_data, x='Frequency', title=f'Frequency Values Distribution in {segment} Segment', nbins=20, color='RFM_Segment')
    st.plotly_chart(fig_hist_segment_frequency)

    # Histogram of Monetary for the selected segment
    fig_hist_segment_monetary = px.histogram(segment_data, x='Monetary', title=f'Monetary Values Distribution in {segment} Segment', nbins=20, color='RFM_Segment')
    st.plotly_chart(fig_hist_segment_monetary)

    # Box plot of RFM Values for the selected segment
    fig_box_segment_rfm = px.box(segment_data, x='RFM_Segment', y='Recency', title=f'Recency Values in {segment} Segment', color='RFM_Segment')
    st.plotly_chart(fig_box_segment_rfm)

elif analysis_type == "Correlation Matrix of RFM Values within Champions Segment":
    st.markdown("""
        <div class='segment'>
            <h3>Correlation Matrix of RFM Values within Champions Segment</h3>
            <p>Analyze the correlation matrix of RFM values within the Champions segment.</p>
        </div>
    """, unsafe_allow_html=True)
    
    champions_data = rfm[rfm['RFM_Segment'] == 'Champions']

    # Correlation matrix
    corr_matrix = champions_data[['Recency', 'Frequency', 'Monetary']].corr()
    fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", title='Correlation Matrix of RFM Values within Champions Segment')
    st.plotly_chart(fig_corr)

# Chatbot integration
st.markdown("""
<div class='segment'>
    <h3>Need help?</h3>
    <p>Chat with our support team for assistance.</p>
</div>
""", unsafe_allow_html=True)

# Add chatbot iframe
components.iframe("https://embed.tawk.to/64a54c80cc26a871b022f26b/1h4vfj13v", height=430)
