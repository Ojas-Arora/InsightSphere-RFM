# RFM-Analysis-Dashboard

![image](https://github.com/user-attachments/assets/ec8767f0-08ed-41d1-baa2-9fcc6bcbac55)

![image](https://github.com/user-attachments/assets/446f4c51-f5e3-4fd0-a508-2357b458cea4)

I. Introduction

The RFM Analysis Dashboard is a powerful tool designed to help businesses understand their customer base by segmenting customers based on three key metrics: Recency, Frequency, and Monetary value (RFM). By leveraging this analysis, businesses can gain insights into customer behavior, identify high-value customers, and tailor marketing strategies to enhance customer engagement and loyalty.

II. What is RFM Analysis?

RFM analysis is a marketing technique used to quantitatively rank and segment customers based on their transaction history. It is based on the following metrics:

1. Recency (R): How recently a customer made a purchase. Customers who recently made a purchase are more likely to buy again compared to those who made a purchase a long time ago.
2. Frequency (F): How often a customer makes a purchase. Customers who purchase more frequently are generally more loyal and potentially more valuable.
3. Monetary Value (M): How much money a customer has spent. Customers who spend more are considered more valuable to the business.
   
III. How the Dashboard Works

1. Data Loading and Preprocessing:

The dashboard starts by loading customer transaction data, including customer IDs, purchase dates, order IDs, and transaction amounts.
The purchase dates are converted to a datetime format, and a reference date is set for calculating the recency of purchases.

2. RFM Metrics Calculation:

The data is grouped by customer ID to calculate the recency, frequency, and monetary value for each customer.
Recency is calculated as the number of days since the customer's last purchase.
Frequency is calculated as the total number of orders made by the customer.
Monetary value is calculated as the total amount spent by the customer.

3. RFM Scoring:

Customers are assigned scores for recency, frequency, and monetary value. These scores are typically divided into quartiles (1 to 4) where:
For recency, a lower score indicates a more recent purchase.
For frequency and monetary value, a higher score indicates more frequent purchases and higher spending, respectively.
The R, F, and M scores are combined to form an overall RFM score and segment.
Customer Segmentation:

Based on their RFM scores, customers are categorized into segments such as "Champions," "Loyal Customers," "Potential Loyalists," "Recent Customers," "Promising," "Need Attention," "At Risk," and "Lost."

4. Visualization and Insights:

The dashboard provides visual representations of the data, including bar charts and histograms, to show the distribution of customers across different RFM segments.
Users can interact with the dashboard to explore various aspects of the data, such as comparing different segments or analyzing the distribution of RFM values within specific segments.
Benefits of RFM Analysis
Targeted Marketing: By understanding which customers are most valuable, businesses can tailor their marketing efforts to retain high-value customers and re-engage those at risk of churn.
Customer Loyalty: Identifying loyal customers helps in creating reward programs that enhance customer loyalty and increase repeat purchases.
Resource Allocation: Businesses can allocate resources more efficiently by focusing on high-value customers and improving strategies for lower-value segments.

V. Conclusion

The RFM Analysis Dashboard is a valuable tool for any business looking to leverage customer data for better decision-making. By using RFM analysis, businesses can gain deeper insights into customer behavior, enhance marketing strategies, and ultimately drive growth and profitability.

VI. How to Use the Dashboard

1. Install Dependencies: Ensure you have Python and the required libraries installed. You can install the necessary packages using:

pip install pandas plotly streamlit

2. Run the Dashboard: Execute the Streamlit app by running:

streamlit run your_dashboard_script.py

3. Explore the Dashboard: Interact with the various features and visualizations to gain insights into your customer segments.

You can view this deployment at 
[RFM Dashboard](https://rfmdashboardpy-9abkamsxruurkcwdb7ydzs.streamlit.app/) 
with the given dataset rfm_data.csv used
