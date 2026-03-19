# ============================================================
# Product Return and Cancellation Analysis in E-commerce
# ============================================================
# This script performs data loading, cleaning, feature engineering,
# analysis, and visualization on an e-commerce orders dataset.
# ============================================================

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend — remove this line to see popup plots
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Set visual style for all plots
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'font.size': 11
})


# ============================================================
# STEP 1: Load Dataset
# ============================================================
print("=" * 60)
print("STEP 1: Loading Dataset")
print("=" * 60)

df = pd.read_csv("ecommerce_orders.csv")

print(f"Dataset loaded successfully!")
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nColumn Names: {list(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head().to_string(index=False))
print(f"\nData Types:\n{df.dtypes}")


# ============================================================
# STEP 2: Data Cleaning
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: Data Cleaning")
print("=" * 60)

# --- 2a. Remove Duplicates ---
duplicates_before = df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(f"Duplicates found and removed: {duplicates_before}")

# --- 2b. Handle Missing Values ---
print(f"\nMissing values BEFORE handling:")
print(df.isnull().sum())

# For 'Delivery Date' and 'Return Date', missing values are expected:
#   - Cancelled orders won't have a Delivery Date
#   - Non-returned orders won't have a Return Date
# We keep them as NaT (Not a Time) after conversion, which is appropriate.
# For numeric columns, fill missing values with 0 if any exist.
if df['Price'].isnull().sum() > 0:
    df['Price'].fillna(0, inplace=True)

print(f"\n(Note: Missing 'Delivery Date' and 'Return Date' values are")
print(f" expected for cancelled/non-returned orders — kept as NaT.)")

# --- 2c. Convert Date Columns to datetime ---
date_columns = ['Order Date', 'Delivery Date', 'Return Date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='coerce')

print(f"\nDate columns converted to datetime format.")
print(f"\nData Types AFTER cleaning:\n{df.dtypes}")


# ============================================================
# STEP 3: Feature Engineering
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: Feature Engineering")
print("=" * 60)

# --- 3a. Delivery Time (in days) ---
# Number of days between Order Date and Delivery Date
df['Delivery Time (days)'] = (df['Delivery Date'] - df['Order Date']).dt.days

# --- 3b. Return Time (in days) ---
# Number of days between Delivery Date and Return Date
df['Return Time (days)'] = (df['Return Date'] - df['Delivery Date']).dt.days

# --- 3c. Order Week ---
# ISO calendar week number extracted from Order Date
df['Order Week'] = df['Order Date'].dt.isocalendar().week.astype('Int64')

print("New features created:")
print("  • Delivery Time (days) = Delivery Date − Order Date")
print("  • Return Time (days)   = Return Date − Delivery Date")
print("  • Order Week           = Week number from Order Date")
print(f"\nSample of new features:")
print(df[['Order ID', 'Order Status', 'Delivery Time (days)',
          'Return Time (days)', 'Order Week']].head(10).to_string(index=False))


# ============================================================
# STEP 4: Analysis
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: Analysis")
print("=" * 60)

total_orders = len(df)
returned_orders = len(df[df['Order Status'] == 'Returned'])
cancelled_orders = len(df[df['Order Status'] == 'Cancelled'])
delivered_orders = len(df[df['Order Status'] == 'Delivered'])

# --- 4a. Return Rate ---
return_rate = (returned_orders / total_orders) * 100
print(f"\n📊 Return Rate: {return_rate:.2f}% ({returned_orders}/{total_orders} orders)")

# --- 4b. Cancellation Rate ---
cancellation_rate = (cancelled_orders / total_orders) * 100
print(f"📊 Cancellation Rate: {cancellation_rate:.2f}% ({cancelled_orders}/{total_orders} orders)")

# --- 4c. Average Return Time ---
avg_return_time = df['Return Time (days)'].mean()
print(f"📊 Average Return Time: {avg_return_time:.1f} days")

# --- 4d. Category with Highest Returns ---
returns_by_category = df[df['Order Status'] == 'Returned']['Product Category'].value_counts()
top_return_category = returns_by_category.idxmax()
top_return_count = returns_by_category.max()
print(f"📊 Highest Returns Category: {top_return_category} ({top_return_count} returns)")

print(f"\nReturns by Category:")
print(returns_by_category.to_string())

# --- 4e. Weekly Trends ---
weekly_returns = (
    df[df['Order Status'] == 'Returned']
    .groupby('Order Week')
    .size()
    .reset_index(name='Returns')
)
weekly_cancellations = (
    df[df['Order Status'] == 'Cancelled']
    .groupby('Order Week')
    .size()
    .reset_index(name='Cancellations')
)

# Merge weekly data for trend analysis
weekly_trends = pd.merge(weekly_returns, weekly_cancellations,
                         on='Order Week', how='outer').fillna(0)
weekly_trends = weekly_trends.sort_values('Order Week')
weekly_trends['Returns'] = weekly_trends['Returns'].astype(int)
weekly_trends['Cancellations'] = weekly_trends['Cancellations'].astype(int)

print(f"\nWeekly Trends (Returns & Cancellations):")
print(weekly_trends.to_string(index=False))


# ============================================================
# STEP 5: Visualizations
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: Creating Visualizations")
print("=" * 60)

# --- 5a. Line Chart: Weekly Returns and Cancellations ---
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(weekly_trends['Order Week'], weekly_trends['Returns'],
         marker='o', linewidth=2, color='#e74c3c', label='Returns', markersize=8)
ax1.plot(weekly_trends['Order Week'], weekly_trends['Cancellations'],
         marker='s', linewidth=2, color='#f39c12', label='Cancellations', markersize=8)
ax1.set_title('Weekly Returns and Cancellations Trend', fontsize=15, fontweight='bold')
ax1.set_xlabel('Week Number')
ax1.set_ylabel('Count')
ax1.legend(frameon=True, shadow=True)
ax1.set_xticks(weekly_trends['Order Week'].values)
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('weekly_trends_line_chart.png', dpi=150, bbox_inches='tight')
plt.show()
print("  ✅ Saved: weekly_trends_line_chart.png")

# --- 5b. Bar Chart: Returns by Product Category ---
fig2, ax2 = plt.subplots(figsize=(9, 5))
colors = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6', '#f1c40f']
bars = ax2.bar(returns_by_category.index, returns_by_category.values,
               color=colors[:len(returns_by_category)], edgecolor='white', linewidth=1.5)

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=12)

ax2.set_title('Returns by Product Category', fontsize=15, fontweight='bold')
ax2.set_xlabel('Product Category')
ax2.set_ylabel('Number of Returns')
ax2.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('returns_by_category_bar_chart.png', dpi=150, bbox_inches='tight')
plt.show()
print("  ✅ Saved: returns_by_category_bar_chart.png")

# --- 5c. Pie Chart: Order Status Distribution ---
status_counts = df['Order Status'].value_counts()
fig3, ax3 = plt.subplots(figsize=(8, 6))
pie_colors = ['#2ecc71', '#e74c3c', '#f39c12']
explode = [0.03, 0.06, 0.06]  # Slightly separate returned & cancelled slices

wedges, texts, autotexts = ax3.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct='%1.1f%%',
    colors=pie_colors,
    explode=explode,
    startangle=140,
    textprops={'fontsize': 12},
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)
for autotext in autotexts:
    autotext.set_fontweight('bold')

ax3.set_title('Order Status Distribution', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('order_status_pie_chart.png', dpi=150, bbox_inches='tight')
plt.show()
print("  ✅ Saved: order_status_pie_chart.png")


# ============================================================
# STEP 6: Key Insights Summary
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: KEY INSIGHTS")
print("=" * 60)

print(f"""
╔══════════════════════════════════════════════════════════╗
║           E-COMMERCE RETURN & CANCELLATION              ║
║                   ANALYSIS SUMMARY                      ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Total Orders Analyzed : {total_orders:<30} ║
║  Delivered Orders      : {delivered_orders:<30} ║
║  Returned Orders       : {returned_orders:<30} ║
║  Cancelled Orders      : {cancelled_orders:<30} ║
║                                                          ║
║  Return Rate           : {return_rate:.2f}%{'':<25} ║
║  Cancellation Rate     : {cancellation_rate:.2f}%{'':<24} ║
║  Average Return Time   : {avg_return_time:.1f} days{'':<22} ║
║                                                          ║
║  Top Return Category   : {top_return_category:<30} ║
║  (with {top_return_count} returns)                                  ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  RECOMMENDATIONS:                                        ║
║  1. Investigate quality issues in '{top_return_category}'{'':<13} ║
║     category to reduce return rates.                     ║
║  2. Review cancellation reasons — {cancellation_rate:.1f}% orders{'':<8} ║
║     are being cancelled before delivery.                 ║
║  3. Avg return time of {avg_return_time:.0f} days suggests customers  ║
║     decide quickly; improve product descriptions.        ║
╚══════════════════════════════════════════════════════════╝
""")


# ============================================================
# STEP 7: Save Cleaned Dataset
# ============================================================
print("=" * 60)
print("STEP 7: Saving Cleaned Dataset")
print("=" * 60)

output_filename = 'ecommerce_orders_cleaned.csv'
df.to_csv(output_filename, index=False)
print(f"  ✅ Cleaned dataset saved as: {output_filename}")
print(f"  📁 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  📋 Columns: {list(df.columns)}")

print("\n" + "=" * 60)
print("✅ ANALYSIS COMPLETE!")
print("=" * 60)
