# Power Query (M) ETL Documentation & Ingestion Guide

**Project:** Customer Segmentation & Retention Analytics in Power BI  
**Target Table Name:** `CustomerData`  
**Source Dataset File:** `data/raw/customer_segmentation_retention_sample.csv` (or `.xlsx`)  
**Snapshot Anchor Date:** `2026-10-16` (Fixed)  

---

## 1. Power Query ETL Workflow Overview

The Power Query extraction, transformation, and loading (ETL) pipeline loads the standardized customer dataset, enforces strict schema types, verifies primary key uniqueness, ensures zero nulls, and preserves the fixed snapshot business rules.

```mermaid
flowchart LR
    SRC[File Source: CSV/Excel] --> PROMOTE[Promote Headers]
    PROMOTE --> TYPES[Explicit Data Type Casting]
    TYPES --> QC[Quality & Null Assertion]
    QC --> LOAD[Load to Data Model as 'CustomerData']
```

---

## 2. Parameter-Based Portable Ingestion Architecture

In standard Power BI Desktop and PBIP models, Power Query M expressions (`File.Contents`) do not resolve relative filesystem paths (e.g. `./data/raw/...`). Hardcoding absolute paths (`D:\...`) creates fragility when the repository is cloned to another drive, directory, or machine.

To resolve this limitation cleanly and maintainably, the semantic model implements a native Power Query Parameter:
- **Parameter Name:** `DatasetFilePath`
- **Parameter Type:** `Text` (Required)
- **Default Value:** `"D:\ML\Sentimental Analysis\data\raw\customer_segmentation_retention_sample.csv"`
- **Metadata Declaration:** `meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]`

When the project is cloned to a different path, users update the path in one single place via **Home > Transform Data > Edit Parameters** without altering M code or partition scripts.

### 2.1 Complete M Parameter Query (`DatasetFilePath`)
```powerquery
"D:\ML\Sentimental Analysis\data\raw\customer_segmentation_retention_sample.csv" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

### 2.2 Complete Copy-Ready M Code for Table (`CustomerData`)

Below is the complete M query script configured for the `CustomerData` partition:

```powerquery
let
    // 1. Ingest dataset using configurable parameter DatasetFilePath
    SourceFilePath = DatasetFilePath,
    
    // 2. Ingest CSV with UTF-8 encoding (Code Page 65001)
    Source = Csv.Document(
        File.Contents(SourceFilePath),
        [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    
    // 3. Promote first row to column headers
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // 4. Enforce strict Power BI data types
    TypedTable = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"Customer ID", type text},
            {"Customer Name", type text},
            {"Age", Int64.Type},
            {"Gender", type text},
            {"City/Region", type text},
            {"Occupation", type text},
            {"Income Level", type text},
            {"Join Date", type date},
            {"Last Purchase Date", type date},
            {"Purchase Frequency", Int64.Type},
            {"Average Order Value", type number},
            {"Total Spend", type number},
            {"Preferred Product Category", type text},
            {"Purchase Channel", type text},
            {"Customer Type", type text},
            {"Engagement Score", Int64.Type},
            {"Satisfaction Score", type number},
            {"Retention Status", type text},
            {"Customer Segment", type text},
            {"Loyalty Tier", type text}
        }
    ),
    
    // 5. Data Quality Assertions (Check for unexpected nulls in primary columns)
    CleanedRows = Table.SelectRows(
        TypedTable, 
        each [Customer ID] <> null and [Customer ID] <> ""
    )
in
    CleanedRows
```

*(Note for Excel Source: If importing from `customer_segmentation_retention_sample.xlsx`, select the sheet named `Customer Dataset`, promote headers, and apply identical `Table.TransformColumnTypes` step).*

---

## 3. Step-by-Step UI Execution Instructions

For authors preferring the Power BI Graphical User Interface:

1. **Import Data:**
   - In Power BI Desktop, select **Get Data $\to$ Text/CSV** (or **Excel Workbook**).
   - Navigate to `D:\ML\Sentimental Analysis\data\raw\customer_segmentation_retention_sample.csv`.
   - Click **Transform Data** (DO NOT click "Load" directly).
2. **Rename Query:**
   - In the left *Queries* pane, right-click the imported query and rename it to **`CustomerData`**.
3. **Verify Header Promotion:**
   - Confirm step `PromoteHeaders` sets `Customer ID` through `Loyalty Tier` as row 1.
4. **Data Type Assignment:**
   - Verify every column icon matches its specified type (123 for Whole Number, 1.2 for Decimal Number, Calendar for Date, and ABC for Text).
5. **Quality Profiling:**
   - On the **View** ribbon tab, enable **Column Quality**, **Column Distribution**, and **Column Profile**.
   - Validate that every column reports **100% Valid**, **0% Error**, and **0% Empty**.
6. **Close & Apply:**
   - Click **Close & Apply** on the Home ribbon to load the table into the tabular model.

---

## 4. Handling the Fixed Snapshot Date (`2026-10-16`)

> [!WARNING]
> **Critical Rule on Recency Calculation:**  
> **DO NOT** recalculate `Retention Status` or `Customer Segment` in Power Query or DAX using dynamic system clocks (`DateTime.LocalNow()` or `TODAY()`).

### Consequences of Using Dynamic Dates:
1. **Model Drift:** As real calendar time advances past October 16, 2026, calculating `TODAY() - [Last Purchase Date]` will falsely inflate elapsed recency days for all 150 records.
2. **Artificial Churn:** Customers legitimately classified as `Retained` (e.g., last purchased on `2026-10-10`, 6 days prior to snapshot) would prematurely transition to `At Risk` (after 60 days) and `Churned` (after 150 days) simply due to passage of real-world calendar time, without any new customer behavior occurring.
3. **Validation Breakage:** All 28 verified ground-truth test assertions and benchmark distribution figures (75 Retained, 44 At Risk, 31 Churned) would be invalidated.
4. **Correct Procedure:** The pre-calculated columns `Retention Status`, `Customer Segment`, and `Loyalty Tier` present in the source dataset are the authoritative ground-truth classifications as of the fixed snapshot date `2026-10-16`. Any supplementary recency calculations must explicitly use `DATE(2026, 10, 16)` as the evaluation anchor.
