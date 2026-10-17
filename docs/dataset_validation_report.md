# Dataset Validation Report

**Project:** Customer Segmentation & Retention Analytics in Power BI  
**Execution Date:** 2026-10-16  
**Evaluator:** Senior Developer  
**Status:** **PASSED (28 / 28 Checks Succeeded — 100% Compliance)**  

---

## 1. Executive Summary

A reproducible synthetic customer dataset consisting of exactly **150 fictional records** and **20 attributes** was generated and validated in `D:\ML\Sentimental Analysis`. The dataset models retail customer behavioral patterns across Indian geographies, denominating financial measures in Indian Rupees (INR - ₹).

All records satisfy deterministic business rules, strict range bounds, arithmetic spend integrity, and deterministic segment assignments as of the fixed snapshot date **October 16, 2026**.

---

## 2. Deliverable Verification Matrix

| Deliverable File | Target Path | Actual Status | Verification Details |
| :--- | :--- | :---: | :--- |
| **Raw CSV Dataset** | [`data/raw/customer_segmentation_retention_sample.csv`](file:///D:/ML/Sentimental%20Analysis/data/raw/customer_segmentation_retention_sample.csv) | **Verified [OK]** | 150 rows $\times$ 20 columns, UTF-8 encoded, 0 nulls. |
| **Raw Excel Workbook** | [`data/raw/customer_segmentation_retention_sample.xlsx`](file:///D:/ML/Sentimental%20Analysis/data/raw/customer_segmentation_retention_sample.xlsx) | **Verified [OK]** | Dual sheets (`Customer Dataset` & `Data Dictionary`) with currency formatting. |
| **Data Dictionary** | [`data/data_dictionary.md`](file:///D:/ML/Sentimental%20Analysis/data/data_dictionary.md) | **Verified [OK]** | 20 attribute definitions, formulas, and data typing rules. |
| **Generator Script** | [`scripts/generate_dataset.py`](file:///D:/ML/Sentimental%20Analysis/scripts/generate_dataset.py) | **Verified [OK]** | Reproducible generation engine (Seed: `42`). |
| **Validator Script** | [`scripts/validate_dataset.py`](file:///D:/ML/Sentimental%20Analysis/scripts/validate_dataset.py) | **Verified [OK]** | Automated 28-point compliance check suite. |

---

## 3. Detailed Validation Results (28 / 28 Checks)

```
--- 1. File Existence & Loading ---
[PASS] CSV Existence: Found: D:\ML\Sentimental Analysis\data\raw\customer_segmentation_retention_sample.csv
[PASS] Excel Existence: Found: D:\ML\Sentimental Analysis\data\raw\customer_segmentation_retention_sample.xlsx
[PASS] CSV Parsing: Parsed 150 records
[PASS] Excel Sheet Verification: Sheets present: ['Customer Dataset', 'Data Dictionary']
[PASS] Excel Customer Dataset Parsing: Parsed 150 records

--- 2. Record & Column Counts ---
[PASS] CSV Row Count: Expected 150, got 150
[PASS] CSV Column Count: Expected 20, got 20
[PASS] Excel Row Count: Expected 150, got 150
[PASS] Excel Column Count: Expected 20, got 20

--- 3. Schema & Column Names ---
[PASS] CSV Column Names: All 20 expected columns match exactly
[PASS] Excel Column Names: All 20 expected columns match exactly

--- 4. Primary Keys & Completeness ---
[PASS] Customer ID Uniqueness: 150 unique IDs for 150 records
[PASS] Customer ID Non-Blank: Found 0 blank IDs
[PASS] Zero Missing / Null Values: Total null values: 0

--- 5. Business Rules & Logic Integrity ---
[PASS] Rule: Age Range [18, 90]: Invalid age records: 0
[PASS] Rule: Positive Purchase Frequency: Non-positive frequency records: 0
[PASS] Rule: Nonnegative Average Order Value: Negative AOV records: 0
[PASS] Rule: Total Spend Math Integrity (Freq * AOV): Mismatched spend records (tolerance > 0.01): 0
[PASS] Rule: Last Purchase Date <= Snapshot Date (2026-10-16): Purchases after snapshot: 0
[PASS] Rule: Join Date <= Last Purchase Date: Join date after last purchase records: 0
[PASS] Rule: Customer Type Calculation: Mismatched customer type records: 0
[PASS] Rule: Retention Status Calculation (Recency Brackets): Mismatched retention status records: 0
[PASS] Rule: Loyalty Tier Calculation (Spend Brackets): Mismatched loyalty tier records: 0
[PASS] Rule: Customer Segment Calculation (Deterministic & Exclusive): Mismatched customer segment records: 0
[PASS] Rule: Engagement Score Range [1, 100]: Invalid engagement score records: 0
[PASS] Rule: Satisfaction Score Range [1.0, 5.0]: Invalid satisfaction score records: 0

--- 6. CSV vs Excel Data Consistency ---
[PASS] CSV vs Excel Parity: 100% cell-by-cell match across all 150 rows

--- 7. Generator Determinism & Reproducibility ---
[PASS] Seed Reproducibility: Independent re-runs with seed=42 yield bit-for-bit identical DataFrames
```

---

## 4. Actual Metric Distributions & Empirical Breakdown

### 4.1. Retention Status Counts
| Retention Status | Recency Criterion | Customer Count | Percentage |
| :--- | :--- | :---: | :---: |
| **Retained** | $0 \le \text{Days} \le 60$ | 75 | 50.0% |
| **At Risk** | $61 \le \text{Days} \le 150$ | 44 | 29.3% |
| **Churned** | $\text{Days} > 150$ | 31 | 20.7% |
| **Total** | — | **150** | **100.0%** |

### 4.2. Customer Segment Distribution
| Customer Segment | Strategic Definition | Customer Count | Percentage |
| :--- | :--- | :---: | :---: |
| **Champions** | High spend (Gold/Plat), high frequency ($\ge 5$), active ($\le 60\text{d}$) | 32 | 21.3% |
| **Loyal Customers** | Steady spend (Silver+), active ($\le 60\text{d}$) | 28 | 18.7% |
| **New / Potential Loyalist** | Recent first-time buyers ($N=1$) or low-ticket active accounts | 25 | 16.7% |
| **Needs Nurturing** | Inactive ($61\text{-}150\text{d}$), lower spend, returning accounts | 23 | 15.3% |
| **At Risk - High Value** | High lifetime spend (Gold/Plat), slipping or churned ($>60\text{d}$) | 22 | 14.7% |
| **Hibernating** | Lapsed accounts ($>150\text{d}$), low/moderate lifetime spend | 20 | 13.3% |
| **Total** | — | **150** | **100.0%** |

### 4.3. Loyalty Tier Breakdown
| Loyalty Tier | Total Spend Threshold (INR) | Customer Count | Percentage |
| :--- | :--- | :---: | :---: |
| **Silver** | $₹15,000 \le \text{Spend} < ₹40,000$ | 47 | 31.3% |
| **Bronze** | $\text{Spend} < ₹15,000$ | 36 | 24.0% |
| **Gold** | $₹40,000 \le \text{Spend} < ₹80,000$ | 34 | 22.7% |
| **Platinum** | $\text{Spend} \ge ₹80,000$ | 33 | 22.0% |
| **Total** | — | **150** | **100.0%** |

### 4.4. Customer Lifecycle Breakdown
| Customer Type | Frequency Rule | Customer Count | Percentage |
| :--- | :--- | :---: | :---: |
| **Returning** | $\text{Purchase Frequency} > 1$ | 125 | 83.3% |
| **New** | $\text{Purchase Frequency} = 1$ | 25 | 16.7% |
| **Total** | — | **150** | **100.0%** |

---

## 5. Execution Commands

To reproduce and validate the dataset independently:

```powershell
# 1. Generate the dataset (CSV and Excel)
& "D:\ML\python\python.exe" scripts/generate_dataset.py

# 2. Run the 28-point automated validation test suite
& "D:\ML\python\python.exe" scripts/validate_dataset.py
```

---

## 6. Known Assumptions & Analytical Limitations

1. **Synthetic Nature**: All 150 customer names and attributes are algorithmically synthesized; no personally identifiable information (PII) or confidential customer records are present.
2. **Snapshot-Level Scope**: The dataset is a point-in-time analytical summary as of **2026-10-16**. It does not contain transaction-level ledger entries (e.g. order item details, tax breakdowns, daily checkout timestamps).
3. **Longitudinal Analytical Boundaries**: Without transaction logs, longitudinal cohort analysis (such as month-over-month retention curves or acquisition vintage analysis) cannot be independently simulated without generating an underlying order history ledger.
