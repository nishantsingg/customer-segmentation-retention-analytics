# Dataset Specification: Customer Segmentation & Retention Analytics

## 1. Project Context & Scope Alignment

> [!NOTE]
> **Specification Reconciliation Notice:**  
> The root directory name (`Sentimental Analysis`) reflects a legacy initialization. In alignment with project requirements, the active project is **Customer Segmentation & Retention Analytics in Power BI**. This document formally supersedes the initial generic text-classification placeholder with the comprehensive, validated customer segmentation dataset specifications.

---

## 2. Dataset Overview

- **Dataset Role**: Ground truth customer snapshot for Power BI segmentation, RFM analysis, loyalty profiling, and retention modeling.
- **Record Count**: Exactly 150 fictional records.
- **Attribute Count**: 20 attributes (demographic, behavioral, monetary, and derived classifications).
- **Snapshot Date**: `2026-10-16` (Fixed anchor for recency and retention classification).
- **Base Currency**: Indian Rupee (INR - ₹).
- **Primary Data Sources**:
  - CSV Format: [`data/raw/customer_segmentation_retention_sample.csv`](file:///D:/ML/Sentimental%20Analysis/data/raw/customer_segmentation_retention_sample.csv)
  - Excel Format: [`data/raw/customer_segmentation_retention_sample.xlsx`](file:///D:/ML/Sentimental%20Analysis/data/raw/customer_segmentation_retention_sample.xlsx) (Sheets: `Customer Dataset`, `Data Dictionary`)

---

## 3. Attribute Schema & Typing

| Column Name | Storage Type | Nullable | Domain / Value Space | Validation Criteria |
| :--- | :--- | :---: | :--- | :--- |
| `Customer ID` | Text / String | No | Unique identifier (`IND-1001` to `IND-1150`) | Regex `^IND-\d{4}$`; 150 unique values |
| `Customer Name` | Text / String | No | Synthesized Indian full names | Non-empty string, no PII |
| `Age` | Integer | No | Adult age in years | Range: $[18, 90]$ |
| `Gender` | Text | No | `Male`, `Female`, `Other` | Categorical membership |
| `City/Region` | Text | No | Indian Cities with State identifier | Format: `"City, State"` |
| `Occupation` | Text | No | Professional occupation | Standardized list of 14 professions |
| `Income Level` | Text | No | Annual household gross income bracket | 4 brackets: Low, Lower-Mid, Upper-Mid, High |
| `Join Date` | Date (`YYYY-MM-DD`) | No | Account registration date | ISO 8601; $\le \text{Last Purchase Date}$ |
| `Last Purchase Date` | Date (`YYYY-MM-DD`) | No | Most recent transaction date | $\ge \text{Join Date}$ and $\le \text{2026-10-16}$ |
| `Purchase Frequency` | Integer | No | Lifetime completed orders count | Positive integer ($\ge 1$) |
| `Average Order Value` | Decimal | No | Mean order spend in INR (₹) | Float $\ge 0.00$, rounded to 2 decimals |
| `Total Spend` | Decimal | No | Lifetime cumulative gross spend (₹) | $\text{Freq} \times \text{AOV} \pm 0.01$ rounding tolerance |
| `Preferred Product Category` | Text | No | 7 core retail categories | Categorical membership |
| `Purchase Channel` | Text | No | `Mobile App`, `Website`, `In-Store`, `Omnichannel` | Categorical membership |
| `Customer Type` | Text | No | `New` (Frequency $= 1$) or `Returning` (Frequency $> 1$) | Deterministic from `Purchase Frequency` |
| `Engagement Score` | Integer | No | Digital interaction score | Integer in $[1, 100]$ |
| `Satisfaction Score` | Decimal | No | Customer satisfaction score (CSAT) | Decimal in $[1.0, 5.0]$ |
| `Retention Status` | Text | No | `Retained`, `At Risk`, `Churned` | Deterministic from recency days |
| `Customer Segment` | Text | No | 6 strategic RFM behavioral clusters | Deterministic mutually exclusive rules |
| `Loyalty Tier` | Text | No | `Bronze`, `Silver`, `Gold`, `Platinum` | Deterministic from `Total Spend` |

---

## 4. Business Logic & Derived Classification Formulas

### 4.1. Arithmetic Spend Integrity
$$\text{Total Spend} = \text{round}(\text{Purchase Frequency} \times \text{Average Order Value}, 2)$$
*(Tolerance: absolute delta $\le 0.01$ allowed for IEEE 754 floating-point precision).*

### 4.2. Retention Status (Recency-based)
Given $\text{Recency Days} = \text{Date}(2026, 10, 16) - \text{Last Purchase Date}$:
- **Retained**: $0 \le \text{Recency Days} \le 60$
- **At Risk**: $61 \le \text{Recency Days} \le 150$
- **Churned**: $\text{Recency Days} > 150$

### 4.3. Loyalty Tier (Spend-based)
- **Bronze**: $\text{Total Spend} < ₹15,000.00$
- **Silver**: $₹15,000.00 \le \text{Total Spend} < ₹40,000.00$
- **Gold**: $₹40,000.00 \le \text{Total Spend} < ₹80,000.00$
- **Platinum**: $\text{Total Spend} \ge ₹80,000.00$

### 4.4. Mutually Exclusive Customer Segmentation
Every customer is deterministically assigned to exactly one of six strategic segments:
1. **Champions**: Active ($\le 60\text{d}$) + High Value (Gold or Platinum) + High Frequency ($\ge 5$).
2. **Loyal Customers**: Active ($\le 60\text{d}$) + Mid/High Value (Silver, Gold, or Platinum) + Frequency $< 5$.
3. **New / Potential Loyalist**: (Active + Bronze) OR (At Risk + New customer with $N=1$).
4. **At Risk - High Value**: Lapsing/Lapsed ($> 60\text{d}$) + High Value (Gold or Platinum).
5. **Needs Nurturing**: At Risk ($61\text{-}150\text{d}$) + Returning ($N>1$) + Bronze/Silver.
6. **Hibernating**: Churned ($> 150\text{d}$) + Bronze/Silver.

---

## 5. Execution & Validation Commands

All dataset generation and validation routines are reproducible with the explicit seed `42`:

```powershell
# Regenerate the dataset (both CSV and Excel)
& "D:\ML\python\python.exe" scripts/generate_dataset.py

# Run full 28-point automated validation suite
& "D:\ML\python\python.exe" scripts/validate_dataset.py
```

---

## 6. Analytical Scope & Known Limitations

> [!CAUTION]
> **Customer Snapshot vs. Transaction-Level History:**
> This dataset provides an aggregated customer-level analytical snapshot as of October 16, 2026.
> 1. **No Granular Ledger**: Individual checkout timestamps, line items, and invoice IDs are not modeled.
> 2. **Longitudinal Limitations**: It does not directly support genuine month-over-month acquisition cohort retention curves or revenue velocity trends without transaction-level expansion.
> 3. **Static Model**: Predictive churn modeling or time-series forecasting cannot be claimed on this static snapshot alone.
