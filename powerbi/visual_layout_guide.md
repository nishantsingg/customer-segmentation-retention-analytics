# Visual Layout Guide & Canvas Coordinate Reference

**Project:** Customer Segmentation & Retention Analytics in Power BI  
**Target Format:** Power BI Desktop Canvas (16:9 Widescreen, $1280 \times 720$ px)  
**Theme File:** [`powerbi/theme.json`](file:///D:/ML/Sentimental%20Analysis/powerbi/theme.json)  
**Project File:** [`powerbi/Customer_Segmentation_Retention.pbip`](file:///D:/ML/Sentimental%20Analysis/powerbi/Customer_Segmentation_Retention.pbip)  

---

## 1. Canvas Layout & Coordinate Maps

### 1.1. Page 1: Customer Overview

```
+----------------------------------------------------------------------------------------------------+
| Header & Mandatory Synthetic Notice Banner  [X:20, Y:15, W:1240, H:50]                            |
+----------------------------------------------------------------------------------------------------+
| [Total Cust] | [Total Rev]  | [AOV]        | [Repeat Rate] | [Retained %] | [Churn %]              |
| [20,75,190]  | [230,75,190] | [440,75,190] | [650,75,190]  | [860,75,190] | [1070,75,190]          |
+--------------+---------------------------------------------+---------------------------------------+
| Slicers      | Customer Count by Customer Segment          | Customer Distribution by Retention    |
| Panel        | [X:290, Y:180, W:470, H:250]                | Status (Donut) [X:780, Y:180, W:480]  |
| [X:20, Y:180 |---------------------------------------------+---------------------------------------+
| W:250, H:520]| Total Revenue by Product Category           | Total Revenue by Purchase Channel     |
|              | [X:290, Y:445, W:470, H:255]                | (Donut) [X:780, Y:445, W:480, H:255]  |
+--------------+---------------------------------------------+---------------------------------------+
```

#### Page 1 Coordinate Inventory
- **Header Banner:** $X=20, Y=15, W=1240, H=50$
- **KPI Card 1 (Total Customers):** $X=20, Y=75, W=190, H=90$
- **KPI Card 2 (Total Revenue):** $X=230, Y=75, W=190, H=90$
- **KPI Card 3 (Average Order Value):** $X=440, Y=75, W=190, H=90$
- **KPI Card 4 (Repeat Customer Rate):** $X=650, Y=75, W=190, H=90$
- **KPI Card 5 (Retention Status Share):** $X=860, Y=75, W=190, H=90$
- **KPI Card 6 (Churn Status Share):** $X=1070, Y=75, W=190, H=90$
- **Slicers Panel:** $X=20, Y=180, W=250, H=520$
- **Chart 1 (Customers by Segment):** $X=290, Y=180, W=470, H=250$
- **Chart 2 (Retention Distribution):** $X=780, Y=180, W=480, H=250$
- **Chart 3 (Revenue by Category):** $X=290, Y=445, W=470, H=255$
- **Chart 4 (Revenue by Channel):** $X=780, Y=445, W=480, H=255$

---

### 1.2. Page 2: Segmentation & Customer Value

```
+----------------------------------------------------------------------------------------------------+
| Header & Segmentation Value Subtitle Banner [X:20, Y:15, W:1240, H:50]                            |
+------------------------------------+-----------------------------------+---------------------------+
| Avg Spend per Customer [20,75,300] | Avg Purchase Freq [340,75,300]    | Avg Engagement [660,75,300] Avg CSAT [980,75,280] |
+------------------------------------+-----------------------------------+---------------------------+
| Total Revenue by Customer Segment  | Segment Revenue Share % (Donut)                               |
| [X:20, Y:180, W:610, H:250]        | [X:650, Y:180, W:610, H:250]                                  |
+------------------------------------+---------------------------------------------------------------+
| Customer Count & Revenue by Tier   | AOV and Average Customer Spend Comparison                     |
| [X:20, Y:445, W:610, H:255]        | [X:650, Y:445, W:610, H:255]                                  |
+------------------------------------+---------------------------------------------------------------+
```

#### Page 2 Coordinate Inventory
- **Header Banner:** $X=20, Y=15, W=1240, H=50$
- **Card 1 (Avg Spend / Customer):** $X=20, Y=75, W=300, H=90$
- **Card 2 (Avg Purchase Frequency):** $X=340, Y=75, W=300, H=90$
- **Card 3 (Avg Engagement Score):** $X=660, Y=75, W=300, H=90$
- **Card 4 (Avg Satisfaction Score):** $X=980, Y=75, W=280, H=90$
- **Chart 1 (Revenue by Segment):** $X=20, Y=180, W=610, H=250$
- **Chart 2 (Segment Revenue Share):** $X=650, Y=180, W=610, H=250$
- **Chart 3 (Loyalty Tier Combo Chart - Revenue Bars & Customer Count Line):** $X=20, Y=445, W=610, H=255$ (`lineClusteredColumnChart`)
- **Chart 4 (Frequency vs Spend):** $X=650, Y=445, W=610, H=255$

---

### 1.3. Page 3: Retention & Risk

```
+----------------------------------------------------------------------------------------------------+
| Header & Risk Mitigation Strategy Banner [X:20, Y:15, W:1240, H:50]                               |
+---------------------------------+-------------------------------+----------------------------------+
| Retained Cust [20,75,290]       | At-Risk Cust [330,75,290]     | Churned Cust [640,75,290] | At-Risk Share [950,75,310] |
+---------------------------------+-------------------------------+----------------------------------+
| At-Risk Distribution Matrix (Segment x Tier)                    | Revenue & Customers by Status    |
| [X:20, Y:180, W:590, H:220]                                     | [X:630, Y:180, W:630, H:220]     |
+-----------------------------------------------------------------+----------------------------------+
| Customer-Level Risk Audit Table (Prioritized by Total Spend Descending)                            |
| [X:20, Y:415, W:1240, H:285]                                                                       |
+----------------------------------------------------------------------------------------------------+
```

#### Page 3 Coordinate Inventory
- **Header Banner:** $X=20, Y=15, W=1240, H=50$
- **Card 1 (Retained Customers):** $X=20, Y=75, W=290, H=90$
- **Card 2 (At-Risk Customers):** $X=330, Y=75, W=290, H=90$
- **Card 3 (Churned Customers):** $X=640, Y=75, W=290, H=90$
- **Card 4 (Portfolio At-Risk Share):** $X=950, Y=75, W=310, H=90$
- **Matrix 1 (At-Risk Segment $\times$ Tier):** $X=20, Y=180, W=590, H=220$
- **Chart 1 (Revenue & Customers by Status):** $X=630, Y=180, W=630, H=220$
- **Table 1 (Customer Risk Audit Table):** $X=20, Y=415, W=1240, H=285$

---

## 2. Step-by-Step Report Build Sequence

### Option A: Opening the Power BI Project Directly (Native Workflow)
1. Ensure Power BI Desktop is installed on your workstation.
2. Double-click [`powerbi/Customer_Segmentation_Retention.pbip`](file:///D:/ML/Sentimental%20Analysis/powerbi/Customer_Segmentation_Retention.pbip).
3. Power BI Desktop will natively parse the report definition (`report.json`) and semantic model (`model.bim`).
4. Click **Refresh** to execute the M partition loading `data/raw/customer_segmentation_retention_sample.csv`.
5. All three report pages will render with pre-configured cards, charts, slicers, and tables.

### Option B: Manual Construction in Power BI Desktop
1. **Load Data:**
   - In Power BI Desktop, navigate to **Home $\to$ Get Data $\to$ Text/CSV**.
   - Select `data/raw/customer_segmentation_retention_sample.csv`.
   - In Power Query, paste the validated M script from [`powerbi/power_query_steps.md`](file:///D:/ML/Sentimental%20Analysis/powerbi/power_query_steps.md) into Advanced Editor.
   - Click **Close & Apply**.
2. **Apply Theme:**
   - In Power BI Desktop, go to **View $\to$ Themes dropdown $\to$ Browse for themes**.
   - Select [`powerbi/theme.json`](file:///D:/ML/Sentimental%20Analysis/powerbi/theme.json).
3. **Create DAX Measures:**
   - On the Home ribbon, click **Enter Data** and create an empty table named `_Measures`.
   - Copy and paste each of the 17 DAX formulas from [`powerbi/dax_measures.md`](file:///D:/ML/Sentimental%20Analysis/powerbi/dax_measures.md).
   - Set the format strings for each measure as documented.
4. **Construct Visuals:**
   - Follow the coordinate inventory above using the **Format visual $\to$ General $\to$ Properties $\to$ Size & Position** panel ($X, Y, Width, Height$).
   - Bind the corresponding measure to each visual card, chart, and table.
5. **Verify Numbers:**
   - Compare displayed visual numbers against the benchmark table in [`docs/kpi_definitions.md`](file:///D:/ML/Sentimental%20Analysis/docs/kpi_definitions.md).
