# ============================================================
# Programmatic Advertising Performance Dashboard
# Author: Swati Kumari
# Tools: Python, Pandas, Matplotlib, Seaborn
# Dataset: Marketing Spending Dataset (Kaggle)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 1. LOAD DATA
# ============================================================
df = pd.read_csv('data/marketing_data.csv')
print("Shape:", df.shape)
print(df.head())

# ============================================================
# 2. DATA CLEANING & PREPROCESSING
# ============================================================
# Convert date column
df['c_date'] = pd.to_datetime(df['c_date'])

# Standardize campaign names to lowercase
df['campaign_name'] = df['campaign_name'].str.lower()

# Add derived metrics
df['CTR'] = (df['clicks'] / df['impressions']) * 100          # Click Through Rate %
df['CPC'] = df['mark_spent'] / df['clicks']                   # Cost Per Click
df['CPL'] = df['mark_spent'] / df['leads'].replace(0, np.nan) # Cost Per Lead
df['ROAS'] = df['revenue'] / df['mark_spent']                 # Return on Ad Spend
df['conversion_rate'] = (df['orders'] / df['clicks']) * 100   # Conversion Rate %

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

print("\nBasic Stats:")
print(df[['impressions', 'mark_spent', 'clicks', 'leads', 'orders', 'revenue']].describe())

# ============================================================
# 3. EXPLORATORY DATA ANALYSIS
# ============================================================

# --- 1. Revenue by Campaign Category ---
plt.figure(figsize=(8, 5))
category_revenue = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
sns.barplot(x=category_revenue.index, y=category_revenue.values, palette='Set2')
plt.title('Total Revenue by Campaign Category')
plt.xlabel('Category')
plt.ylabel('Total Revenue ($)')
plt.tight_layout()
plt.savefig('visuals/revenue_by_category.png')
plt.show()

# --- 2. ROAS by Campaign ---
plt.figure(figsize=(10, 5))
campaign_roas = df.groupby('campaign_name')['ROAS'].mean().sort_values(ascending=False)
sns.barplot(x=campaign_roas.index, y=campaign_roas.values, palette='coolwarm')
plt.title('Average ROAS by Campaign')
plt.xlabel('Campaign')
plt.ylabel('ROAS')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('visuals/roas_by_campaign.png')
plt.show()

# --- 3. Monthly Ad Spend vs Revenue Trend ---
plt.figure(figsize=(12, 5))
monthly = df.groupby(df['c_date'].dt.to_period('M')).agg(
    total_spend=('mark_spent', 'sum'),
    total_revenue=('revenue', 'sum')
).reset_index()
monthly['c_date'] = monthly['c_date'].astype(str)

plt.plot(monthly['c_date'], monthly['total_spend'], marker='o', label='Ad Spend', color='red')
plt.plot(monthly['c_date'], monthly['total_revenue'], marker='o', label='Revenue', color='green')
plt.title('Monthly Ad Spend vs Revenue')
plt.xlabel('Month')
plt.ylabel('Amount ($)')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig('visuals/monthly_spend_vs_revenue.png')
plt.show()

# --- 4. CTR by Campaign Category ---
plt.figure(figsize=(8, 5))
ctr_category = df.groupby('category')['CTR'].mean().sort_values(ascending=False)
sns.barplot(x=ctr_category.index, y=ctr_category.values, palette='Blues_d')
plt.title('Average CTR by Campaign Category')
plt.xlabel('Category')
plt.ylabel('CTR (%)')
plt.tight_layout()
plt.savefig('visuals/ctr_by_category.png')
plt.show()

# --- 5. Budget Pacing - Spend Distribution by Campaign ---
plt.figure(figsize=(10, 5))
spend_campaign = df.groupby('campaign_name')['mark_spent'].sum().sort_values(ascending=False)
sns.barplot(x=spend_campaign.index, y=spend_campaign.values, palette='magma')
plt.title('Total Ad Spend by Campaign')
plt.xlabel('Campaign')
plt.ylabel('Total Spend ($)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('visuals/spend_by_campaign.png')
plt.show()

# ============================================================
# 4. KPI SUMMARY
# ============================================================
print("\n========== KPI SUMMARY ==========")
print(f"Total Impressions: {df['impressions'].sum():,.0f}")
print(f"Total Ad Spend: ${df['mark_spent'].sum():,.2f}")
print(f"Total Revenue: ${df['revenue'].sum():,.2f}")
print(f"Total Clicks: {df['clicks'].sum():,.0f}")
print(f"Total Orders: {df['orders'].sum():,.0f}")
print(f"Overall CTR: {df['CTR'].mean():.2f}%")
print(f"Overall ROAS: {df['ROAS'].mean():.2f}")
print(f"Overall CPC: ${df['CPC'].mean():.2f}")
print(f"Overall Conversion Rate: {df['conversion_rate'].mean():.2f}%")
