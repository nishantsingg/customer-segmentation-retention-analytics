# DAX Measure Library: Customer Segmentation & Retention Analytics

**Project:** Customer Segmentation & Retention Analytics in Power BI  
**Target Table Name:** `CustomerData`  
**Measures Table:** `_Measures` (Recommended dedicated container)  
**Snapshot Anchor Date:** `2026-10-16`  
**Base Currency:** Indian Rupee (INR - ₹)  

---

## 1. Overview & Measure Governance

All analytical KPIs in this portfolio project are implemented as explicit DAX measures rather than calculated columns or default visual aggregations. This ensures:
1. Dynamic recalculation under arbitrary slicer contexts (demographics, geography, channel).
2. Elimination of divide-by-zero errors through strict use of `DIVIDE()`.
3. Clear architectural separation between the raw customer entity table (`CustomerData`) and business logic calculations.

---

## 2. Core Financial & Volume Measures

### 2.1. `[Total Customers]`
```dax
Total Customers = 
DISTINCTCOUNT(CustomerData[Customer ID])
```
- **Business Definition:** Count of unique customer accounts active within the snapshot dataset.
- **Format String:** `#,##0`
- **Expected Filter Behavior:** Dynamically reflects slicers applied to `Customer Segment`, `Retention Status`, `City/Region`, etc.
- **Dataset Ground Truth Benchmark:** **150**

---

### 2.2. `[Total Revenue]`
```dax
Total Revenue = 
SUM(CustomerData[Total Spend])
```
- **Business Definition:** Cumulative historical monetary spend generated across all customer accounts in Indian Rupees (INR).
- **Format String:** `₹#,##0.00`
- **Expected Filter Behavior:** Aggregates total lifetime expenditure for all customers currently filtered in context.
- **Dataset Ground Truth Benchmark:** **₹7,368,001.75**

---

### 2.3. `[Total Orders]`
```dax
Total Orders = 
SUM(CustomerData[Purchase Frequency])
```
- **Business Definition:** Total count of completed purchase transactions across all customer accounts in the dataset.
- **Format String:** `#,##0`
- **Expected Filter Behavior:** Aggregates cumulative purchase frequencies for filtered customers.
- **Dataset Ground Truth Benchmark:** **794**

---

### 2.4. `[Average Order Value]`
```dax
Average Order Value = 
DIVIDE(
    [Total Revenue],
    [Total Orders],
    0
)
```
- **Business Definition:** Weighted average transaction value across all completed orders (Total Spend divided by Total Orders).
- **Format String:** `₹#,##0.00`
- **Analytical Note:** This measure calculates the true order-weighted AOV ($₹7,368,001.75 / 794 = ₹9,279.60$). A simple unweighted average of the `Average Order Value` column would yield $₹10,297.73$, skewing upward due to low-frequency high-ticket customers.
- **Dataset Ground Truth Benchmark:** **₹9,279.60**

---

### 2.5. `[Average Customer Spend]`
```dax
Average Customer Spend = 
DIVIDE(
    [Total Revenue],
    [Total Customers],
    0
)
```
- **Business Definition:** Mean cumulative lifetime spend per customer account.
- **Format String:** `₹#,##0.00`
- **Expected Filter Behavior:** Measures the average financial value of a customer within any selected slice.
- **Dataset Ground Truth Benchmark:** **₹49,120.01**

---

### 2.6. `[Average Purchase Frequency]`
```dax
Average Purchase Frequency = 
DIVIDE(
    [Total Orders],
    [Total Customers],
    0
)
```
- **Business Definition:** Mean number of lifetime orders completed per customer.
- **Format String:** `#,##0.00`
- **Expected Filter Behavior:** Indicates average purchase velocity of the customer group in context.
- **Dataset Ground Truth Benchmark:** **5.29**

---

## 3. Customer Behavior & Lifecycle Measures

### 3.1. `[Repeat Customers]`
```dax
Repeat Customers = 
CALCULATE(
    [Total Customers],
    CustomerData[Purchase Frequency] > 1
)
```
- **Business Definition:** Count of customers who have completed more than one purchase transaction (Purchase Frequency $\ge 2$).
- **Format String:** `#,##0`
- **Analytical Note:** In this aggregated snapshot, purchase frequency is an attribute of the customer rather than a row count in a transaction ledger.
- **Dataset Ground Truth Benchmark:** **125**

---

### 3.2. `[Repeat Customer Rate]`
```dax
Repeat Customer Rate = 
DIVIDE(
    [Repeat Customers],
    [Total Customers],
    0
)
```
- **Business Definition:** Proportion of total customers who have made repeat purchases.
- **Format String:** `0.0%`
- **Expected Filter Behavior:** Evaluates customer retention momentum across channels, regions, or segments.
- **Dataset Ground Truth Benchmark:** **83.3%** ($125 / 150$)

---

## 4. Retention & Risk Measures (Snapshot Shares)

> [!IMPORTANT]
> **Snapshot Share Clarification:**  
> These measures represent the distribution of customers across retention categories as of the **October 16, 2026 snapshot date**. They are **not** longitudinal period-over-period cohort retention or churn rates (which require multi-period transaction event logs).

---

### 4.1. `[Retained Customers]`
```dax
Retained Customers = 
CALCULATE(
    [Total Customers],
    CustomerData[Retention Status] = "Retained"
)
```
- **Business Definition:** Count of customers whose last purchase occurred within 0 to 60 days of the snapshot date.
- **Format String:** `#,##0`
- **Dataset Ground Truth Benchmark:** **75**

---

### 4.2. `[Retention Status Share %]`
```dax
Retention Status Share % = 
DIVIDE(
    [Retained Customers],
    CALCULATE([Total Customers], ALL(CustomerData[Retention Status])),
    0
)
```
- **Business Definition:** Proportion of customers categorized as `Retained` relative to the total active customer population.
- **Format String:** `0.0%`
- **Filter Behavior:** Denominator removes filters on `Retention Status` while preserving demographic, regional, and segment filters.
- **Dataset Ground Truth Benchmark:** **50.0%** ($75 / 150$)

---

### 4.3. `[At-Risk Customers]`
```dax
At-Risk Customers = 
CALCULATE(
    [Total Customers],
    CustomerData[Retention Status] = "At Risk"
)
```
- **Business Definition:** Count of customers whose last purchase occurred between 61 and 150 days prior to the snapshot date.
- **Format String:** `#,##0`
- **Dataset Ground Truth Benchmark:** **44**

---

### 4.4. `[At-Risk Status Share %]`
```dax
At-Risk Status Share % = 
DIVIDE(
    [At-Risk Customers],
    CALCULATE([Total Customers], ALL(CustomerData[Retention Status])),
    0
)
```
- **Business Definition:** Proportion of customers categorized as `At Risk` in the snapshot.
- **Format String:** `0.0%`
- **Dataset Ground Truth Benchmark:** **29.3%** ($44 / 150$)

---

### 4.5. `[Churned Customers]`
```dax
Churned Customers = 
CALCULATE(
    [Total Customers],
    CustomerData[Retention Status] = "Churned"
)
```
- **Business Definition:** Count of customers whose last purchase was more than 150 days prior to the snapshot date.
- **Format String:** `#,##0`
- **Dataset Ground Truth Benchmark:** **31**

---

### 4.6. `[Churn Status Share %]`
```dax
Churn Status Share % = 
DIVIDE(
    [Churned Customers],
    CALCULATE([Total Customers], ALL(CustomerData[Retention Status])),
    0
)
```
- **Business Definition:** Proportion of customers categorized as `Churned` in the snapshot.
- **Format String:** `0.0%`
- **Dataset Ground Truth Benchmark:** **20.7%** ($31 / 150$)

---

## 5. Engagement & Customer Value Measures

### 5.1. `[Average Engagement Score]`
```dax
Average Engagement Score = 
AVERAGE(CustomerData[Engagement Score])
```
- **Business Definition:** Mean digital interaction and engagement rating (1 to 100) across filtered customers.
- **Format String:** `0.0`
- **Dataset Ground Truth Benchmark:** **60.0** (59.99 unrounded)

---

### 5.2. `[Average Satisfaction Score]`
```dax
Average Satisfaction Score = 
AVERAGE(CustomerData[Satisfaction Score])
```
- **Business Definition:** Mean customer satisfaction rating (CSAT: 1.0 to 5.0) across filtered customers.
- **Format String:** `0.0`
- **Dataset Ground Truth Benchmark:** **3.7** (3.67 unrounded)

---

### 5.3. `[Segment Revenue Share %]`
```dax
Segment Revenue Share % = 
DIVIDE(
    [Total Revenue],
    CALCULATE(
        [Total Revenue],
        ALL(CustomerData[Customer Segment])
    ),
    0
)
```
- **Business Definition:** Percentage contribution of the selected customer segment to total portfolio revenue.
- **Format String:** `0.0%`
- **Expected Filter Behavior:** The denominator clears any direct filter on `Customer Segment`, ensuring the sum of all segment shares equals 100% when viewed in a segment matrix, while respecting external slicers (e.g., filtering to a specific city or channel).
- **Dataset Ground Truth Benchmarks by Segment:**
  - `Champions`: **46.6%** (₹3,433,209.83)
  - `At Risk - High Value`: **21.8%** (₹1,606,501.29)
  - `Loyal Customers`: **16.5%** (₹1,218,738.85)
  - `Needs Nurturing`: **6.9%** (₹510,982.96)
  - `Hibernating`: **5.4%** (₹400,706.93)
  - `New / Potential Loyalist`: **2.7%** (₹197,861.89)

---

## 6. Analytical Discussion: Estimated Customer Lifetime Value (CLV)

> [!CAUTION]
> **Distinction Between Verified Historical Spend and Forward-Looking CLV:**  
> Historical spend (`[Average Customer Spend] = ₹49,120.01`) represents realized historical cash flow, **not** forward-looking Customer Lifetime Value (CLV).

If executive leadership requests an estimated benchmark CLV heuristic for scenario modeling, it should be formulated as an explicit, separate model metric with clearly stated assumptions:

### Heuristic Model Definition:
$$\text{Estimated Future Annual Value} = \text{Annualized Purchase Frequency} \times \text{AOV} \times \text{Gross Margin \%}$$

```dax
Estimated Annualized Customer Value = 
VAR AssumedGrossMargin = 0.40  // Documented assumption: 40% gross margin
RETURN
DIVIDE(
    [Total Revenue] * AssumedGrossMargin,
    [Total Customers],
    0
)
```

### Necessary Conditions for Rigorous Predictive CLV:
1. **Observation Window:** Requires a multi-year transactional ledger to establish empirical churn hazard rates ($\lambda$) and survival curves $S(t)$.
2. **Defensible Lifespan / Retention Horizon:** Cannot be reliably inferred from a 150-record single-date snapshot without assuming an arbitrary customer lifespan.
3. **Discount Rate:** Applying Net Present Value (NPV) discounting requires defined future cash flow intervals.
4. **Governance Rule:** Do **not** present heuristic annualized spend as actuarial or predictive CLV without explicitly disclosing the underlying margin and horizon assumptions.
