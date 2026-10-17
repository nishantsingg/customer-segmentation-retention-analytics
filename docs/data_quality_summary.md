# Data Quality & Profiling Summary

**Project:** Customer Segmentation & Retention Analytics in Power BI  
**Document Type:** Formal Data Quality & Profiling Assessment  
**Audit Date:** 2026-10-16  
**Audited Assets:**
- `data/raw/customer_segmentation_retention_sample.csv`
- `data/raw/customer_segmentation_retention_sample.xlsx`
**Total Records:** 150  
**Data Integrity Status:** **100% Valid (Zero Defects Detected)**  

---

## 1. Data Quality Dimension Assessment

| Quality Dimension | Standard / Expectation | Measured Result | Evaluation Status |
| :--- | :--- | :--- | :---: |
| **Completeness** | 0 nulls, NaNs, or empty strings across all 20 columns. | 0 missing values detected across 3,000 data cells. | **PASSED [OK]** |
| **Uniqueness** | 100% unique primary keys (`Customer ID`). | 150 distinct IDs (`IND-1001` to `IND-1150`). | **PASSED [OK]** |
| **Validity** | All values adhere to prescribed regex, formats, and ranges. | Age $\in [18, 90]$, Engagement $\in [1, 100]$, CSAT $\in [1.0, 5.0]$. | **PASSED [OK]** |
| **Accuracy / Math** | $\text{Total Spend} = \text{Freq} \times \text{AOV} \pm 0.01$. | 0 records exceeded the rounding tolerance of 0.01. | **PASSED [OK]** |
| **Consistency** | Exact cell-by-cell parity between CSV and Excel tables. | 150 rows $\times$ 20 columns match identically across formats. | **PASSED [OK]** |
| **Timeliness / Logic** | $\text{Join Date} \le \text{Last Purchase Date} \le 2026\text{-}10\text{-}16$. | 100% of dates satisfy temporal precedence constraints. | **PASSED [OK]** |
| **Determinism** | Identical output upon re-running with seed `42`. | Independent re-runs confirmed bit-for-bit reproducibility. | **PASSED [OK]** |

---

## 2. Attribute-Level Profiling Summary

| Attribute | Data Type | Min Value | Max Value | Mean / Mode | Distinct Values | Completeness |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `Customer ID` | Text | `IND-1001` | `IND-1150` | — | 150 | 100% |
| `Customer Name` | Text | — | — | Fictional Full Names | 150 | 100% |
| `Age` | Whole Number | 20 | 75 | 44.4 years | 47 | 100% |
| `Gender` | Text | — | — | `Male` (49.3%), `Female` (44.7%), `Other` (6.0%) | 3 | 100% |
| `City/Region` | Text | — | — | 16 Indian Metro / Tier-1 / Tier-2 Cities | 16 | 100% |
| `Occupation` | Text | — | — | 14 Standard Professions | 14 | 100% |
| `Income Level` | Text | — | — | 4 INR Income Brackets | 4 | 100% |
| `Join Date` | Date | `2024-04-12` | `2026-10-12` | — | 143 | 100% |
| `Last Purchase Date`| Date | `2025-08-25` | `2026-10-14` | Max $\le$ 2026-10-16 | 114 | 100% |
| `Purchase Frequency`| Whole Number | 1 | 18 | 5.29 orders | 18 | 100% |
| `Average Order Value`| Decimal (INR) | ₹1,200.00 | ₹14,500.00 | ₹10,297.73 (simple mean) | 148 | 100% |
| `Total Spend` | Decimal (INR) | ₹1,200.00 | ₹114,996.00 | ₹49,120.01 (mean spend) | 150 | 100% |
| `Preferred Category`| Text | — | — | 7 Core Retail Merchandise Classes | 7 | 100% |
| `Purchase Channel` | Text | — | — | 4 Omnichannel / Digital Paths | 4 | 100% |
| `Customer Type` | Text | — | — | `Returning` (83.3%), `New` (16.7%) | 2 | 100% |
| `Engagement Score` | Whole Number | 5 | 98 | 59.99 / 100 | 73 | 100% |
| `Satisfaction Score`| Decimal | 1.2 | 5.0 | 3.67 / 5.0 | 35 | 100% |
| `Retention Status` | Text | — | — | `Retained` (50%), `At Risk` (29.3%), `Churned` (20.7%) | 3 | 100% |
| `Customer Segment` | Text | — | — | 6 Mutually Exclusive RFM Segments | 6 | 100% |
| `Loyalty Tier` | Text | — | — | `Silver` (31.3%), `Bronze` (24%), `Gold` (22.7%), `Plat` (22%)| 4 | 100% |

---

## 3. Discovered Anomalies & Resolution Log

During the data lifecycle implementation, three operational anomalies were identified, audited, and resolved:

1. **Console Character Encoding on Windows Host:**
   - *Observation:* Validation script crashed when outputting Unicode checkmark symbols (`\u2713`) under host codepage `cp1252`.
   - *Resolution:* Standardized console output logging to ASCII-safe status tags (`[PASS]`, `[FAIL]`, `[OK]`), ensuring cross-platform stability.
2. **Weighted vs. Unweighted Average Order Value (AOV):**
   - *Observation:* Taking the arithmetic mean of the column `Average Order Value` produces $₹10,297.73$, whereas dividing cumulative revenue by cumulative orders yields $₹9,279.60$.
   - *Resolution:* Formally documented this distinction in the DAX measure library. `[Average Order Value]` is implemented as `DIVIDE([Total Revenue], [Total Orders], 0)` to guarantee true volume-weighted mathematical correctness.
3. **Reproducibility Module Resolution:**
   - *Observation:* When validator executed generator re-runs via import, python failed to resolve package relative paths.
   - *Resolution:* Added runtime path injection (`sys.path.insert(0, project_root)`) ensuring deterministic standalone test execution.

---

## 4. Governance Constraints & Analytical Boundaries

1. **Synthetic Nature:**
   - The data is generated solely for portfolio demonstration in Power BI. No customer identities belong to actual individuals or commercial entities.
2. **Point-in-Time Analytical Boundary:**
   - The dataset represents an analytical snapshot fixed at **2026-10-16**.
   - It cannot be updated dynamically using system clocks without corrupting recency classifications.
3. **No Transaction-Level Ledger:**
   - Order-level line items, basket SKUs, and checkout velocity cannot be modeled without synthesizing an underlying transaction ledger.
