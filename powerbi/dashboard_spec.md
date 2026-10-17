# Power BI Dashboard Specification: 3-Page Executive Portfolio Report

**Project:** Customer Segmentation & Retention Analytics in Power BI  
**Report Format:** Power BI Project (`.pbip`) & Implementation Specification  
**Canvas Resolution:** 16:9 Widescreen (1280 $\times$ 720 pixels)  
**Target Table:** `CustomerData`  
**Snapshot Anchor Date:** `2026-10-16`  
**Base Currency:** Indian Rupee (INR - ₹)  
**Palette:** Navy `#183153` | Blue `#2878B5` | Green `#27966B` | Orange `#E8A23A` | Red `#D9534F` | Light Grey `#F3F6FA`  
**Typography:** Segoe UI  

---

## 1. Global Visual & Formatting Standards

1. **Header & Context Banner:** Every page includes a top title bar displaying the page theme and the mandatory notice:  
   *`"Synthetic Retail Portfolio Analytics — Snapshot Date: 2026-10-16"`*
2. **Typography Hierarchy:**
   - Page Titles: 16pt Bold (`#183153`)
   - Visual Titles: 11pt Bold (`#183153`)
   - KPI Callout Numbers: 20pt Bold (`#183153`)
   - KPI Sub-labels: 9.5pt Regular (`#5C6B73`)
   - Axis Labels & Legends: 9pt Regular (`#5C6B73`)
3. **Number Formatting Rules:**
   - Financial Metrics (`Total Revenue`, `AOV`, `Average Spend`): Currency format `₹#,##0.00` (or `₹#,##0` on small cards).
   - Percentages (`Repeat Customer Rate`, `Retention Share`, `Segment Share`): `0.0%` (e.g., `83.3%`, `50.0%`).
   - Counts & Frequencies: Integer format `#,##0`.

---

## 2. Page 1: Customer Overview

**Business Intent:** Provide executive stakeholders with high-level portfolio health, core revenue metrics, segment distribution, and omnichannel mix.

```mermaid
graph TD
    subgraph Page 1 Layout Grid
        BANNER[Header & Synthetic Notice Banner]
        KPI[6 Top KPI Cards: Customers | Revenue | AOV | Repeat Rate | Retained Share | Churn Share]
        SLICER[Left Slicer Panel: Segment, Region, Status, Tier]
        CHART1[Bar: Customers by Segment]
        CHART2[Donut: Customers by Retention Status]
        CHART3[Column: Revenue by Category]
        CHART4[Donut: Revenue by Purchase Channel]
    end
```

### Visual Specifications — Page 1

| Visual ID | Visual Type | Title / Label | Field & Measure Mappings | Target Values (Global) | Formatting & Visual Notes |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **P1-V01** | Textbox | Header Banner | N/A | Static Header | Font 16pt Bold Navy, subtitle 10pt grey. |
| **P1-V02** | KPI Card | Total Customers | `[Total Customers]` | **150** | Segoe UI 20pt Bold. |
| **P1-V03** | KPI Card | Total Revenue | `[Total Revenue]` | **₹7.37M** | Formatted in INR (`₹7,368,001.75`). |
| **P1-V04** | KPI Card | Average Order Value | `[Average Order Value]` | **₹9,279.60** | Order-weighted AOV. |
| **P1-V05** | KPI Card | Repeat Customer Rate | `[Repeat Customer Rate]` | **83.3%** | Accent Color: Blue `#2878B5`. |
| **P1-V06** | KPI Card | Retained Customers (0–60 Days) | `[Retention Status Share %]` (Tooltip: `[Retained Customers]`) | **75 (50.0%)** | Accent Color: Green `#27966B`. Displays active accounts count and share. |
| **P1-V07** | KPI Card | Churned Customers (>150 Days) | `[Churn Status Share %]` (Tooltip: `[Churned Customers]`) | **31 (20.7%)** | Accent Color: Red `#D9534F`. Displays churned accounts count and share. |
| **P1-V08** | Slicer | Filter: Customer Segment | `CustomerData[Customer Segment]` | 6 Segments | Vertical list with multi-select support. |
| **P1-V09** | Clustered Bar | Customer Count by Segment | Y-Axis: `CustomerData[Customer Segment]`<br/>X-Axis: `[Total Customers]` | 32, 28, 25, 23, 22, 20 | Data labels ON, bars colored `#183153`. Sorted by count desc. |
| **P1-V10** | Donut Chart | Retention Status Distribution | Legend: `CustomerData[Retention Status]`<br/>Values: `[Total Customers]` | Retained: 75, At Risk: 44, Churned: 31 | Retained: `#27966B`, At Risk: `#E8A23A`, Churned: `#D9534F`. |
| **P1-V11** | Clustered Column | Revenue by Product Category | X-Axis: `CustomerData[Preferred Product Category]`<br/>Y-Axis: `[Total Revenue]` | 7 Categories | Data labels ON in INR. Sorted by revenue desc. |
| **P1-V12** | Donut Chart | Revenue by Purchase Channel | Legend: `CustomerData[Purchase Channel]`<br/>Values: `[Total Revenue]` | 4 Channels | Slices colored with palette series. |

---

## 3. Page 2: Segmentation & Customer Value

**Business Intent:** Analyze the monetary contribution and behavioral differentiation between customer segments and loyalty tiers to inform commercial campaigns.

### Visual Specifications — Page 2

| Visual ID | Visual Type | Title / Label | Field & Measure Mappings | Target Values (Global) | Formatting & Visual Notes |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **P2-V01** | Textbox | Header Banner | N/A | Static Header | Segment & Value Profiling title. |
| **P2-V02** | KPI Card | Avg Spend per Customer | `[Average Customer Spend]` | **₹49,120.01** | Segoe UI 20pt Bold. |
| **P2-V03** | KPI Card | Avg Purchase Frequency | `[Average Purchase Frequency]` | **5.29 orders** | Numeric card with 2 decimal precision. |
| **P2-V04** | KPI Card | Avg Engagement Score | `[Average Engagement Score]` | **60.0 / 100** | Index tracking digital platform activity. |
| **P2-V05** | KPI Card | Avg Satisfaction (CSAT)| `[Average Satisfaction Score]` | **3.7 / 5.0** | Customer sentiment rating. |
| **P2-V06** | Clustered Bar | Total Revenue by Segment | Y-Axis: `CustomerData[Customer Segment]`<br/>X-Axis: `[Total Revenue]` | Champions: ₹3.43M<br/>At Risk-High: ₹1.61M | Champions generate 46.6% of portfolio spend. |
| **P2-V07** | Donut Chart | Segment Revenue Share % | Legend: `CustomerData[Customer Segment]`<br/>Values: `[Segment Revenue Share %]` | Champions: 46.6%<br/>At Risk-High: 21.8% | Denominator handles external slicers cleanly. |
| **P2-V08** | Combo Chart (`lineClusteredColumnChart`) | Total Revenue (Bars) & Customer Count (Line) by Loyalty Tier | Category (X): `CustomerData[Loyalty Tier]`<br/>Primary Y (Bars): `[Total Revenue]`<br/>Secondary Y (Line): `[Total Customers]` | Platinum: ₹3.79M (33)<br/>Gold: ₹2.08M (34)<br/>Silver: ₹1.07M (49)<br/>Bronze: ₹0.43M (34) | Dual-axis combo chart. Solves scale mismatch (₹3.79M vs 33) so both revenue volume and customer counts are interpretable. Tier order: Platinum $\to$ Gold $\to$ Silver $\to$ Bronze. |
| **P2-V09** | Clustered Column | AOV & Spend Comparison | X-Axis: `CustomerData[Customer Segment]`<br/>Y-Axis: `[Average Order Value]`, `[Average Customer Spend]` | Compare ticket size vs annual value | Dual column series: AOV (`#2878B5`), Avg Spend (`#183153`). |

---

## 4. Page 3: Retention & Risk

**Business Intent:** Proactively flag churn vulnerabilities, prioritize high-value lapsing accounts, and provide an actionable customer drill-down table.

### Visual Specifications — Page 3

| Visual ID | Visual Type | Title / Label | Field & Measure Mappings | Target Values (Global) | Formatting & Visual Notes |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **P3-V01** | Textbox | Header Banner | N/A | Static Header | Retention Risk & Health Monitoring. |
| **P3-V02** | KPI Card | Retained Customers | `[Retained Customers]` | **75 (50.0%)** | Green accent `#27966B`. Active (0-60d). |
| **P3-V03** | KPI Card | At-Risk Customers | `[At-Risk Customers]` | **44 (29.3%)** | Orange accent `#E8A23A`. Inactive (61-150d). |
| **P3-V04** | KPI Card | Churned Customers | `[Churned Customers]` | **31 (20.7%)** | Red accent `#D9534F`. Inactive (>150d). |
| **P3-V05** | KPI Card | Portfolio At-Risk Share| `[At-Risk Status Share %]`| **29.3%** | Key risk indicator callout. |
| **P3-V06** | Matrix Visual | At-Risk Distribution by Segment & Tier | Rows: `Customer Segment`<br/>Columns: `Loyalty Tier`<br/>Values: `[At-Risk Customers]` | 22 in High-Value (Gold/Plat) | Highlights urgent winback targets. |
| **P3-V07** | Clustered Bar | Status Revenue & Count Analysis | Y-Axis: `CustomerData[Retention Status]`<br/>X-Axis: `[Total Revenue]` & `[Total Customers]` | Retained: ₹4.78M<br/>At Risk: ₹1.88M | Demonstrates revenue at risk. |
| **P3-V08** | Detailed Table | Customer-Level Risk Audit Table | Columns: `Customer ID`, `Customer Name`, `City/Region`, `Last Purchase Date`, `Retention Status`, `Customer Segment`, `Total Spend`, `Purchase Frequency` | 150 rows drillable | Sorted by `Total Spend` DESC. Top rows highlight most valuable customers. |

---

## 5. Filter Interaction & Cross-Filtering Behavior

1. **Page 1 Cross-Filtering:**
   - Clicking a segment bar (e.g. `Champions`) highlights retention status, category spend, and channel mix for Champions only.
   - Slicer selection (`City/Region`) recalculates all KPI cards dynamically without breaking ratios.
2. **Page 3 Priority Slicing:**
   - Filter `Retention Status` can be toggled to `At Risk` to immediately filter the Customer Audit Table to the 44 at-risk accounts.
   - Cross-filtering by `Loyalty Tier = Platinum` isolates the top priority high-value accounts requiring concierge outreach.
