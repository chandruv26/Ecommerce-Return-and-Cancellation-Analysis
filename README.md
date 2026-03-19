# 📊 Product Return and Cancellation Analysis in E-commerce

A Python-based data analysis project that explores patterns in e-commerce order returns and cancellations. The project performs data cleaning, feature engineering, statistical analysis, and generates visualizations to uncover actionable business insights.

---

## 🎯 Objective

Analyze e-commerce order data to:
- Identify return and cancellation rates
- Discover which product categories have the highest returns
- Track weekly trends in returns and cancellations
- Provide data-driven recommendations to reduce losses

---

## 📁 Dataset

The dataset (`ecommerce_orders.csv`) contains the following columns:

| Column | Description |
|--------|-------------|
| Order ID | Unique identifier for each order |
| Product Category | Category of the product (Electronics, Clothing, Beauty, Home & Kitchen, Books) |
| Order Date | Date when the order was placed |
| Delivery Date | Date when the order was delivered |
| Return Date | Date when the product was returned (if applicable) |
| Order Status | Current status — Delivered, Returned, or Cancelled |
| Price | Price of the product (in ₹) |

---

## 🛠️ Technologies Used

- **Python 3**
- **Pandas** — Data manipulation and cleaning
- **Matplotlib** — Data visualization
- **Seaborn** — Statistical data visualization

---

## ⚙️ Steps Performed

1. **Data Loading** — Load CSV dataset using Pandas
2. **Data Cleaning** — Remove duplicates, handle missing values, convert date columns
3. **Feature Engineering** — Create new columns:
   - `Delivery Time (days)` = Delivery Date − Order Date
   - `Return Time (days)` = Return Date − Delivery Date
   - `Order Week` = Week number from Order Date
4. **Analysis** — Calculate return rate, cancellation rate, average return time, category-wise returns, weekly trends
5. **Visualization** — Generate line chart, bar chart, and pie chart
6. **Insights** — Print key findings and recommendations
7. **Export** — Save cleaned dataset as `ecommerce_orders_cleaned.csv`

---

## 📈 Visualizations

### Weekly Returns and Cancellations Trend
> Line chart showing how returns and cancellations fluctuate across weeks.

### Returns by Product Category
> Bar chart comparing total returns across different product categories.

### Order Status Distribution
> Pie chart showing the proportion of Delivered, Returned, and Cancelled orders.

---

## 🔍 Key Insights

| Metric | Value |
|--------|-------|
| Total Orders | 50 |
| Return Rate | 28.00% |
| Cancellation Rate | 16.00% |
| Average Return Time | 4.0 days |
| Top Return Category | Clothing |

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/chandruv26/Ecommerce-Return-and-Cancellation-Analysis.git
   cd Ecommerce-Return-and-Cancellation-Analysis
   ```

2. **Install dependencies**
   ```bash
   pip install pandas matplotlib seaborn
   ```

3. **Run the analysis**
   ```bash
   python analysis.py
   ```

4. **Output files generated:**
   - `ecommerce_orders_cleaned.csv`
   - `weekly_trends_line_chart.png`
   - `returns_by_category_bar_chart.png`
   - `order_status_pie_chart.png`

---

## 📂 Project Structure

```
├── analysis.py                  # Main Python analysis script
├── ecommerce_orders.csv         # Raw dataset
├── ecommerce_orders_cleaned.csv # Cleaned dataset (auto-generated)
├── weekly_trends_line_chart.png # Line chart (auto-generated)
├── returns_by_category_bar_chart.png # Bar chart (auto-generated)
├── order_status_pie_chart.png   # Pie chart (auto-generated)
├── .gitignore
└── README.md
```

---

## 👤 Author

**Chandru V**
- GitHub: [@chandruv26](https://github.com/chandruv26)

---

## 📜 License

This project is open source and available for educational purposes.
