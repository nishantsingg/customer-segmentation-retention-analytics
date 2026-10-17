import pandas as pd
import numpy as np

def main():
    csv_path = "data/raw/customer_segmentation_retention_sample.csv"
    df = pd.read_csv(csv_path)

    total_customers = len(df)
    total_spend = df["Total Spend"].sum()
    total_orders = df["Purchase Frequency"].sum()
    aov_weighted = total_spend / total_orders
    simple_mean_aov = df["Average Order Value"].mean()
    avg_spend_per_cust = total_spend / total_customers
    avg_orders_per_cust = total_orders / total_customers
    repeat_cust = (df["Purchase Frequency"] > 1).sum()
    repeat_rate = repeat_cust / total_customers
    new_cust = (df["Purchase Frequency"] == 1).sum()
    new_rate = new_cust / total_customers

    print("=== DATASET SHAPE & TOTALS ===")
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Total Historical Spend (Revenue): INR {total_spend:,.2f}")
    print(f"Total Purchase Frequency (Orders): {total_orders:,}")
    print(f"Weighted Average Order Value (Total Spend / Total Orders): INR {aov_weighted:,.2f}")
    print(f"Simple Average of AOV Column: INR {simple_mean_aov:,.2f}")
    print(f"Average Spend per Customer: INR {avg_spend_per_cust:,.2f}")
    print(f"Average Purchase Frequency per Customer: {avg_orders_per_cust:.2f}")
    print(f"Repeat Customers (Freq > 1): {repeat_cust} ({repeat_rate:.2%})")
    print(f"New Customers (Freq == 1): {new_cust} ({new_rate:.2%})")
    print(f"Average Engagement Score: {df['Engagement Score'].mean():.2f}")
    print(f"Average Satisfaction Score: {df['Satisfaction Score'].mean():.2f}")

    print("\n=== RETENTION STATUS COUNTS & SHARES ===")
    ret = df["Retention Status"].value_counts()
    for k, v in ret.items():
        print(f"  - {k:15}: {v:3} ({v/total_customers:6.2%})")

    print("\n=== CUSTOMER SEGMENT COUNTS, SPEND & REVENUE SHARE ===")
    seg_stats = df.groupby("Customer Segment").agg(
        Count=("Customer ID", "count"),
        Total_Spend=("Total Spend", "sum"),
        Total_Orders=("Purchase Frequency", "sum"),
        Avg_Engagement=("Engagement Score", "mean"),
        Avg_CSAT=("Satisfaction Score", "mean")
    )
    seg_stats["Cust_Share"] = seg_stats["Count"] / total_customers
    seg_stats["Rev_Share"] = seg_stats["Total_Spend"] / total_spend
    seg_stats["AOV"] = seg_stats["Total_Spend"] / seg_stats["Total_Orders"]
    seg_stats["Spend_Per_Cust"] = seg_stats["Total_Spend"] / seg_stats["Count"]

    for seg, row in seg_stats.iterrows():
        print(f"  - {seg:25}: Count={row['Count']:2.0f} ({row['Cust_Share']:5.2%}) | Spend=INR {row['Total_Spend']:10,.2f} ({row['Rev_Share']:5.2%}) | AOV=INR {row['AOV']:8,.2f}")

    print("\n=== LOYALTY TIER COUNTS, SPEND & SHARES ===")
    tier_stats = df.groupby("Loyalty Tier").agg(
        Count=("Customer ID", "count"),
        Total_Spend=("Total Spend", "sum")
    )
    tier_stats["Cust_Share"] = tier_stats["Count"] / total_customers
    tier_stats["Rev_Share"] = tier_stats["Total_Spend"] / total_spend
    for tier, row in tier_stats.iterrows():
        print(f"  - {tier:12}: Count={row['Count']:2.0f} ({row['Cust_Share']:5.2%}) | Spend=INR {row['Total_Spend']:10,.2f} ({row['Rev_Share']:5.2%})")

    print("\n=== CUSTOMER TYPE COUNTS & SHARES ===")
    type_stats = df.groupby("Customer Type").agg(
        Count=("Customer ID", "count"),
        Total_Spend=("Total Spend", "sum")
    )
    type_stats["Cust_Share"] = type_stats["Count"] / total_customers
    type_stats["Rev_Share"] = type_stats["Total_Spend"] / total_spend
    for ctype, row in type_stats.iterrows():
        print(f"  - {ctype:12}: Count={row['Count']:2.0f} ({row['Cust_Share']:5.2%}) | Spend=INR {row['Total_Spend']:10,.2f} ({row['Rev_Share']:5.2%})")

if __name__ == "__main__":
    main()
