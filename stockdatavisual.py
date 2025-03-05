import streamlit as st
import pymysql
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def connect_to_database():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="abcd",
        database="STOCKMARKET",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_stock_data(query):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(data)

    return df

def get_unique_values(df, column):
    return sorted(df[column].unique().tolist())

def main():
    st.title("Data-Driven Stock Analysis")
    
    query = """SELECT * FROM tblsectorstocks"""

    merged_df = fetch_stock_data(query)
    
    ######################### Market Summary ############################
    st.header("Market Summary")
        
    green_stocks_count = merged_df[merged_df['yearly_return'] >= 0]['Ticker'].nunique()
    red_stocks_count = merged_df[merged_df['yearly_return'] < 0]['Ticker'].nunique()
    avg_price = merged_df['close'].mean()
    avg_volume = merged_df['volume'].mean()

    col1, col2 = st.columns(2)
    col1.metric(f"Number of Green Stocks", f"{green_stocks_count}")
    col2.metric(f"Number of Red Stocks", f"{red_stocks_count}")
    col3, col4 = st.columns(2)
    col3.metric(f"Average Price Across All Stocks", f"{avg_price:.2f}")
    col4.metric(f"Average Volume Across All Stocks", f"{avg_volume:.2f}")

    col5, col6 = st.columns(2)
    
    with col5:
    ######################### Top 10 Green Stocks ############################
        top_10_green_stocks = merged_df.drop_duplicates(subset=['Ticker']).sort_values(by='yearly_return', ascending=False, ignore_index=True).head(10)
        st.header("Top 10 Green Stocks")
        st.dataframe(top_10_green_stocks[['Ticker', 'yearly_return']],hide_index=True)

    with col6:
    ######################### Top 10 Loss Stocks ############################
        top_10_red_stocks = merged_df.drop_duplicates(subset=['Ticker']).sort_values(by='yearly_return', ignore_index=True).head(10)
        st.header("Top 10 Loss Stocks") 
        st.dataframe(top_10_red_stocks[['Ticker', 'yearly_return']],hide_index=True)

    ######################### Top 10 Most Volatile Stocks ###################################################

    st.header("Top 10 Most Volatile Stocks")
    volatility = merged_df.groupby('Ticker')['daily_return'].std()

    top_10_volatility = volatility.sort_values(ascending=False).head(10)

    plt.figure(figsize=(6, 6))
    sns.barplot(x=top_10_volatility.index, y=top_10_volatility.values, hue=top_10_volatility.index, palette='RdYlGn', legend=False)
    plt.title('Top 10 Most Volatile Stocks')
    plt.xlabel('Ticker')
    plt.ylabel('Volatility (Standard Deviation)')
    plt.xticks(rotation=45)
    plt.tight_layout()  
    st.pyplot(plt)
    st.write("**Insights :** Volatility gives insight into how much the price fluctuates, which is valuable for risk assessment. Higher volatility often indicates more risk, while lower volatility indicates a more stable stock.")
    st.write("**ADANIENT,ADANIPORTS and BEL** Companies are having high volatility in given data, which has more risk compared to other stocks.")
    st.write("**NTPC,HINDALCO and COALINDIA** Companies are having lower volatility in given data, which has less risk compared to other stocks.")

    ######################### Cumulative Return for Top 5 Performing Stocks #############################################
    st.header("Cumulative Return for Top 5 Stocks")
    top_5_CRstocks = merged_df.groupby('Ticker')['cumulative_return'].last().nlargest(5).index

    plt.figure(figsize=(12, 8))
    for ticker in top_5_CRstocks:
        stock_data = merged_df[merged_df['Ticker'] == ticker]
        sns.lineplot(data=stock_data, x='date', y='cumulative_return', label=ticker)

    plt.title('Cumulative Return for Top 5 Performing Stocks')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.tight_layout()  
    st.pyplot(plt)
    st.write("**Insights :** The cumulative return is an important metric to visualize overall performance and growth over time. This helps users compare how different stocks performed relative to each other.")
    st.write("**TRENT** Company overall performance and growth over time is good compared to other stocks.")

    ######################### Average Yearly Return by Sector #############################################
    st.header("Average Yearly Return by Sector")
    
    sector_avg_df = merged_df.groupby("Sector")["yearly_return"].mean().reset_index()

    plt.figure(figsize=(12, 8))
    sns.barplot(data=sector_avg_df, x="Sector", y="yearly_return", hue="Sector")

    plt.title('Average Yearly Return by Sector', fontsize=16)
    plt.xlabel('Sector', fontsize=12)
    plt.ylabel('Average Yearly Return (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout() 
    st.pyplot(plt)
    st.write("**Insights :** Stock performance by sector to gauge market sentiment in specific industries.")
    st.write("**DEFENCE, RETAILING and TELECOM** sector's average yearly returns are more compared to other sectors, which indicates higher profit in yearly inverstment.")
    st.write("**FMCG, PAINTS, TRADING and FOOD & TOBACCO** sector's average yearly return goes less than zero, which indicates loss in yearly inverstment.")

    ######################### Stock Price Correlation Heatmap #############################################
    st.header("Stock Price Correlation Heatmap")

    stock_prices = merged_df.pivot(index='date', columns='Ticker', values='close')
    correlation_matrix = stock_prices.corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', cbar=True)
    plt.title('Stock Price Correlation Heatmap')
    plt.tight_layout()  

    st.pyplot(plt)
    st.write("**Insights :** Many stocks like **HDFCBANK & ICICIBANK, TCS & INFY, and BAJAJ-AUTO & HEROMOTOCO** show strong positive correlations (deep red areas), indicating that they move in tandem. These could be stocks from the same industry or sector")
    st.write("Some stocks like **NTPC and POWERGRID** have near-zero correlations, suggesting they move independently.")
    st.write("Some stock pairs like **ITC or HINDUNILVR** exhibit negative correlations, indicating they move in opposite directions.")
    ######################### Top 5 Gainers and Losers (Month-wise) #############################################
    st.header("Top 5 Gainers and Losers (Month-wise)")

    for month in merged_df['month'].unique():
        month_data = merged_df[merged_df['month'] == month]

        month_data_unique = month_data.drop_duplicates(subset=['Ticker'])

        st.subheader(f"Month: {month}")
        
        if len(month_data_unique) >= 5:
            top_5_gainers = month_data_unique.nlargest(5, 'monthly_return')
            top_5_losers = month_data_unique.nsmallest(5, 'monthly_return')
            
            top_5_gainers['Category'] = 'Top 5 Gainers'
            top_5_losers['Category'] = 'Top 5 Losers'
        
            fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)
            
            sns.barplot(x='Ticker', y='monthly_return', data=top_5_gainers, ax=axes[0], palette='Greens_d', hue='Ticker')
            axes[0].set_title(f'Top 5 Gainers - {month}')
            axes[0].set_xlabel('Ticker')
            axes[0].set_ylabel('Monthly Return (%)')
            axes[0].tick_params(axis='x', rotation=45)

            sns.barplot(x='Ticker', y='monthly_return', data=top_5_losers, ax=axes[1], palette='Reds_d', hue='Ticker')
            axes[1].set_title(f'Top 5 Losers - {month}')
            axes[1].set_xlabel('Ticker')
            axes[1].tick_params(axis='x', rotation=45)

            plt.tight_layout()  
            st.pyplot(plt)

    # st.write("**Insights :** History, Musical and Sport genres lead in popularity, receiving the highest votes among all genres.")

if __name__ == "__main__":
    main()
