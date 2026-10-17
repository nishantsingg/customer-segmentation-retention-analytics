# Power BI Project Compatibility, Runtime, and Functional Audit

**Project:** Customer Segmentation & Retention Analytics in Power BI  
**Workspace:** `D:\ML\Sentimental Analysis`  
**Audit Date:** 2026-10-16  
**Auditor:** Senior Developer  
**Audit Engine:** [`scripts/validate_powerbi_project.py`](file:///D:/ML/Sentimental%20Analysis/scripts/validate_powerbi_project.py)  
**Overall Status:** **ALL 31 AUDIT CHECKS PASSED [OK] (100% Structural & Semantic Compliance)**  

---

## 1. Executive Summary

This audit evaluates the architectural completeness, schema fidelity, DAX correctness, and data source portability of the Power BI Project (`.pbip`) deliverables.

### Testing Boundary Declaration
> [!IMPORTANT]
> **Static Architectural Audit vs. Live Desktop UI Execution:**
> - **Power BI Desktop Application:** The host environment was audited for Power BI Desktop executables (`PBIDesktop.exe` in `C:\Program Files` and Microsoft Store packages). **Power BI Desktop is NOT installed on this host.**
> - **No Simulated Desktop Claims:** We make **no claim** that Power BI Desktop executed or rendered these visuals locally. No fabricated screenshots or synthetic mockups were produced.
> - **Verification Scope:** All structural artifacts (`.pbip`, `.pbir`, `.pbism`, `model.bim`, `report.json`, `theme.json`), 17 DAX formulas, M partitions, and 29 visual containers were audited and verified using automated static analysis and Python mathematical modeling.

---

## 2. Phase 1: Power BI Project Structure Audit

The workspace contains a complete, standards-compliant Microsoft Power BI Project (`.pbip`) structure:

```
powerbi/
├── Customer_Segmentation_Retention.pbip              [Master Project Pointer]
├── theme.json                                       [Corporate Hex Theme & Typography]
├── Customer_Segmentation_Retention.Report/
│   ├── definition.pbir                              [Dataset Reference Pointer]
│   └── report.json                                  [3 Pages, 29 Visual Containers]
└── Customer_Segmentation_Retention.SemanticModel/
    ├── definition.pbism                             [Semantic Model Descriptor]
    └── model.bim                                    [Analysis Services TMSL Tabular Schema]
```

| Component | Target File | Audit Finding | Status |
| :--- | :--- | :--- | :---: |
| **PBIP Pointer** | `Customer_Segmentation_Retention.pbip` | References `Customer_Segmentation_Retention.Report` with `enableAutoAuth: true`. | **PASS [OK]** |
| **PBIR Definition** | `Customer_Segmentation_Retention.Report/definition.pbir` | Relative path `../Customer_Segmentation_Retention.SemanticModel` correctly bound. | **PASS [OK]** |
| **PBISM Descriptor**| `Customer_Segmentation_Retention.SemanticModel/definition.pbism` | Valid schema version 1.0. | **PASS [OK]** |
| **Tabular Schema**  | `Customer_Segmentation_Retention.SemanticModel/model.bim` | Compatibility level `1550`, culture `en-US`, 20 columns, 17 measures. | **PASS [OK]** |
| **Report Layout**   | `Customer_Segmentation_Retention.Report/report.json` | 3 sections, 29 valid visual containers, 100% valid queryRefs. | **PASS [OK]** |
| **Corporate Theme** | `powerbi/theme.json` | Corporate palette (`#183153`, `#2878B5`, `#27966B`, `#E8A23A`, `#D9534F`), Segoe UI font. | **PASS [OK]** |

---

## 3. Phase 2: Data Source & Partition Configuration Audit

### 3.1. Parameterized Ingestion & M Partition Evaluation
The M expression in `model.bim` consumes a dedicated Power Query parameter query (`DatasetFilePath`) declaring:
```powerquery
"D:\ML\Sentimental Analysis\data\raw\customer_segmentation_retention_sample.csv" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

The table partition query references this parameter:
```powerquery
let
    // 1. Ingest dataset using configurable parameter DatasetFilePath
    SourceFilePath = DatasetFilePath,
    Source = Csv.Document(File.Contents(SourceFilePath), [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedTable = Table.TransformColumnTypes(PromotedHeaders, {
        {"Customer ID", type text}, {"Customer Name", type text}, {"Age", Int64.Type},
        {"Gender", type text}, {"City/Region", type text}, {"Occupation", type text},
        {"Income Level", type text}, {"Join Date", type date}, {"Last Purchase Date", type date},
        {"Purchase Frequency", Int64.Type}, {"Average Order Value", type number},
        {"Total Spend", type number}, {"Preferred Product Category", type text},
        {"Purchase Channel", type text}, {"Customer Type", type text},
        {"Engagement Score", Int64.Type}, {"Satisfaction Score", type number},
        {"Retention Status", type text}, {"Customer Segment", type text},
        {"Loyalty Tier", type text}
    }),
    CleanedRows = Table.SelectRows(TypedTable, each [Customer ID] <> null and [Customer ID] <> "")
in
    CleanedRows
```

### 3.2. Data Source Audit Findings
1. **Physical File Availability:** The underlying file [`data/raw/customer_segmentation_retention_sample.csv`](file:///D:/ML/Sentimental%20Analysis/data/raw/customer_segmentation_retention_sample.csv) is confirmed present on disk (150 rows, 20 columns, UTF-8 encoded).
2. **Encoding Safety:** The partition explicitly specifies `Encoding=65001` (UTF-8), preventing character corruption on regional Windows machines.
3. **Zero Embedded Secrets:** No passwords, access tokens, API keys, or tenant credentials are embedded.
4. **Path Portability & Parameter-Driven Migration:**
   - In Power BI Desktop and PBIP models, Power Query M expressions (`File.Contents`) cannot resolve relative filesystem paths.
   - To provide seamless portability without manual M code edits, the model registers `DatasetFilePath` as an M parameter query (`IsParameterQuery=true`).
   - **When cloned to a different path or machine:** In Power BI Desktop, click **Home > Transform Data > Edit Parameters**, update `DatasetFilePath` to the local path, and click **Apply Changes**. No partition scripts need to be touched.

---

## 4. Phase 3: DAX Measure Library Audit

All 17 measures registered in `model.bim` were audited for mathematical correctness, safe division, and filter context semantics:

| # | Measure Name | Complete DAX Expression | Format String | Safe Division (`DIVIDE`) | Ground-Truth Benchmark |
| :-: | :--- | :--- | :---: | :---: | :---: |
| **1** | `[Total Customers]` | `DISTINCTCOUNT(CustomerData[Customer ID])` | `#,##0` | N/A | **150** |
| **2** | `[Total Revenue]` | `SUM(CustomerData[Total Spend])` | `"₹"#,##0.00` | N/A | **₹7,368,001.75** |
| **3** | `[Total Orders]` | `SUM(CustomerData[Purchase Frequency])` | `#,##0` | N/A | **794** |
| **4** | `[Average Order Value]` | `DIVIDE([Total Revenue], [Total Orders], 0)` | `"₹"#,##0.00` | **Yes** | **₹9,279.60** |
| **5** | `[Average Customer Spend]` | `DIVIDE([Total Revenue], [Total Customers], 0)` | `"₹"#,##0.00` | **Yes** | **₹49,120.01** |
| **6** | `[Average Purchase Frequency]` | `DIVIDE([Total Orders], [Total Customers], 0)` | `#,##0.00` | **Yes** | **5.29** |
| **7** | `[Repeat Customers]` | `CALCULATE([Total Customers], CustomerData[Purchase Frequency] > 1)` | `#,##0` | N/A | **125** |
| **8** | `[Repeat Customer Rate]` | `DIVIDE([Repeat Customers], [Total Customers], 0)` | `0.0%` | **Yes** | **83.3%** |
| **9** | `[Retained Customers]` | `CALCULATE([Total Customers], CustomerData[Retention Status] = "Retained")` | `#,##0` | N/A | **75** |
| **10**| `[Retention Status Share %]` | `DIVIDE([Retained Customers], CALCULATE([Total Customers], ALL(CustomerData[Retention Status])), 0)` | `0.0%` | **Yes** | **50.0%** |
| **11**| `[At-Risk Customers]` | `CALCULATE([Total Customers], CustomerData[Retention Status] = "At Risk")` | `#,##0` | N/A | **44** |
| **12**| `[At-Risk Status Share %]` | `DIVIDE([At-Risk Customers], CALCULATE([Total Customers], ALL(CustomerData[Retention Status])), 0)` | `0.0%` | **Yes** | **29.3%** |
| **13**| `[Churned Customers]` | `CALCULATE([Total Customers], CustomerData[Retention Status] = "Churned")` | `#,##0` | N/A | **31** |
| **14**| `[Churn Status Share %]` | `DIVIDE([Churned Customers], CALCULATE([Total Customers], ALL(CustomerData[Retention Status])), 0)` | `0.0%` | **Yes** | **20.7%** |
| **15**| `[Average Engagement Score]` | `AVERAGE(CustomerData[Engagement Score])` | `0.0` | N/A | **60.0** (59.99) |
| **16**| `[Average Satisfaction Score]` | `AVERAGE(CustomerData[Satisfaction Score])` | `0.0` | N/A | **3.7** (3.67) |
| **17**| `[Segment Revenue Share %]` | `DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(CustomerData[Customer Segment])), 0)` | `0.0%` | **Yes** | Champions: **46.6%** |

### Key Filter Context Findings:
- **`[Segment Revenue Share %]`:** Accurately removes `Customer Segment` filters using `ALL(CustomerData[Customer Segment])`, allowing relative segment contribution to sum to 100% while respecting external slicers (e.g. City or Channel).
- **Snapshot Shares:** Accurately clear the status dimension filter via `ALL(CustomerData[Retention Status])` to establish current snapshot portfolio distribution without claiming longitudinal cohort retention.

---

## 5. Phase 4: Complete Visual Container Inventory (29 Containers Audited)

Every visual container across all three pages was audited for visual type validity, canvas boundary containment ($1280 \times 720$), and field projection integrity:

| Page Name | Visual Type | Title / Label | Position & Dimensions | Referenced Field / Measure | Audit Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Customer Overview** | `textbox` | Header Banner | $X:20, Y:15, W:1240, H:50$ | Static Header (16pt / 10pt) | **VALID [OK]** |
| **Customer Overview** | `card` | Total Customers | $X:20, Y:75, W:190, H:90$ | `CustomerData.Total Customers` | **VALID [OK]** |
| **Customer Overview** | `card` | Total Revenue (INR) | $X:230, Y:75, W:190, H:90$ | `CustomerData.Total Revenue` | **VALID [OK]** |
| **Customer Overview** | `card` | Average Order Value (AOV) | $X:440, Y:75, W:190, H:90$ | `CustomerData.Average Order Value` | **VALID [OK]** |
| **Customer Overview** | `card` | Repeat Customer Rate | $X:650, Y:75, W:190, H:90$ | `CustomerData.Repeat Customer Rate` | **VALID [OK]** |
| **Customer Overview** | `card` | Retention Status Share | $X:860, Y:75, W:190, H:90$ | `CustomerData.Retention Status Share %`| **VALID [OK]** |
| **Customer Overview** | `card` | Churn Status Share | $X:1070, Y:75, W:190, H:90$ | `CustomerData.Churn Status Share %` | **VALID [OK]** |
| **Customer Overview** | `slicer` | Filter: Customer Segment | $X:20, Y:180, W:250, H:520$ | `CustomerData.Customer Segment` | **VALID [OK]** |
| **Customer Overview** | `clusteredBarChart` | Customer Count by Segment | $X:290, Y:180, W:470, H:250$ | `Customer Segment`, `[Total Customers]`| **VALID [OK]** |
| **Customer Overview** | `pieChart` | Customer Distribution by Retention | $X:780, Y:180, W:480, H:250$ | `Retention Status`, `[Total Customers]` | **VALID [OK]** |
| **Customer Overview** | `clusteredColumnChart`| Revenue by Product Category | $X:290, Y:445, W:470, H:255$ | `Preferred Category`, `[Total Revenue]` | **VALID [OK]** |
| **Customer Overview** | `pieChart` | Revenue by Purchase Channel | $X:780, Y:445, W:480, H:255$ | `Purchase Channel`, `[Total Revenue]` | **VALID [OK]** |
| **Segmentation & Value**| `textbox` | Header Banner P2 | $X:20, Y:15, W:1240, H:50$ | Static Header | **VALID [OK]** |
| **Segmentation & Value**| `card` | Average Spend per Customer | $X:20, Y:75, W:300, H:90$ | `CustomerData.Average Customer Spend` | **VALID [OK]** |
| **Segmentation & Value**| `card` | Average Purchase Frequency | $X:340, Y:75, W:300, H:90$ | `CustomerData.Average Purchase Frequency`| **VALID [OK]** |
| **Segmentation & Value**| `card` | Average Engagement Score | $X:660, Y:75, W:300, H:90$ | `CustomerData.Average Engagement Score`| **VALID [OK]** |
| **Segmentation & Value**| `card` | Average CSAT (1-5) | $X:980, Y:75, W:280, H:90$ | `CustomerData.Average Satisfaction Score`| **VALID [OK]** |
| **Segmentation & Value**| `clusteredBarChart` | Total Revenue by Segment | $X:20, Y:180, W:610, H:250$ | `Customer Segment`, `[Total Revenue]` | **VALID [OK]** |
| **Segmentation & Value**| `pieChart` | Segment Revenue Share % | $X:650, Y:180, W:610, H:250$ | `Customer Segment`, `[Segment Revenue Share %]`| **VALID [OK]** |
| **Segmentation & Value**| `lineClusteredColumnChart`| Loyalty Tier Combo Chart | $X:20, Y:445, W:610, H:255$ | Primary Y (Bars): `[Total Revenue]`, Secondary Y (Line): `[Total Customers]` | **VALID [OK]** |
| **Segmentation & Value**| `clusteredColumnChart`| AOV & Spend Comparison | $X:650, Y:445, W:610, H:255$ | `Customer Segment`, `[AOV]`, `[Average Customer Spend]` | **VALID [OK]** |
| **Retention & Risk** | `textbox` | Header Banner P3 | $X:20, Y:15, W:1240, H:50$ | Static Header | **VALID [OK]** |
| **Retention & Risk** | `card` | Retained Customers (0-60d) | $X:20, Y:75, W:290, H:90$ | `CustomerData.Retained Customers` | **VALID [OK]** |
| **Retention & Risk** | `card` | At-Risk Customers (61-150d)| $X:330, Y:75, W:290, H:90$ | `CustomerData.At-Risk Customers` | **VALID [OK]** |
| **Retention & Risk** | `card` | Churned Customers (>150d) | $X:640, Y:75, W:290, H:90$ | `CustomerData.Churned Customers` | **VALID [OK]** |
| **Retention & Risk** | `card` | Portfolio At-Risk Share % | $X:950, Y:75, W:310, H:90$ | `CustomerData.At-Risk Status Share %` | **VALID [OK]** |
| **Retention & Risk** | `matrix` | At-Risk Segment x Tier | $X:20, Y:180, W:590, H:220$ | Rows: `Segment`, Cols: `Tier`, Val: `[At-Risk Customers]` | **VALID [OK]** |
| **Retention & Risk** | `clusteredBarChart` | Revenue & Count by Status | $X:630, Y:180, W:630, H:220$ | `Retention Status`, `[Total Customers]`, `[Total Revenue]` | **VALID [OK]** |
| **Retention & Risk** | `tableEx` | Customer Risk Audit Table | $X:20, Y:415, W:1240, H:285$| 8 Columns (`ID`, `Name`, `City`, `Date`, `Status`, `Segment`, `Spend`, `Freq`) | **VALID [OK]** |

---

## 6. Discovered Defect & Correction Log

During the initial pass of Phase 4 visual parsing, an anomaly was discovered in `report.json`:
- **Anomaly Description:** The three header textbox visualContainers (`Header_Banner`, `Header_Banner_P2`, `Header_Banner_P3`) contained a malformed JSON closing token (`}}]}}]}}}` instead of `}}]}}]}}`), causing sub-parsers to fail on lines 19, 124, and 205.
- **Root Cause:** A misplaced extra closing curly brace inside the escaped paragraph properties JSON string.
- **Resolution:** Corrected all three textbox configs using a programmatic Python updater, ensuring strict JSON serialization.
- **Rerun Verification:** Rerunning [`scripts/validate_powerbi_project.py`](file:///D:/ML/Sentimental%20Analysis/scripts/validate_powerbi_project.py) confirmed all 29 visual containers parsed as `VALID [OK]`.

---

## 7. Step-by-Step Instructions to Open and Test in Power BI Desktop

To open, refresh, and validate the report on a workstation equipped with **Microsoft Power BI Desktop**:

1. **Launch Project:**
   - Double-click [`powerbi/Customer_Segmentation_Retention.pbip`](file:///D:/ML/Sentimental%20Analysis/powerbi/Customer_Segmentation_Retention.pbip).
   - Power BI Desktop will natively read `report.json` and `model.bim`.
2. **Refresh Dataset:**
   - Click **Refresh** on the Home ribbon tab.
   - Power Query will load the 150 records from `data/raw/customer_segmentation_retention_sample.csv`.
3. **Verify Ground-Truth Scores:**
   - Confirm Page 1 displays: Total Customers = **150**, Total Revenue = **₹7.37M**, AOV = **₹9,279.60**, Repeat Rate = **83.3%**.
   - Confirm Page 2 displays: Champions Revenue Share = **46.6%**, Average Spend = **₹49,120.01**.
   - Confirm Page 3 displays: Retained = **75**, At Risk = **44**, Churned = **31**.
4. **Test Interactive Cross-Filtering:**
   - On Page 1, click the `Champions` bar in *Customer Count by Segment* $\to$ verify that *Retention Distribution* updates to 100% Retained and Revenue updates to ₹3.43M.
   - On Page 3, toggle the *At Risk* filter $\to$ confirm the *Customer Risk Audit Table* isolates the 44 accounts requiring re-engagement.
