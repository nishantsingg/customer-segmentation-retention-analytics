# Customer Segmentation & Retention Analytics in Power BI — Technical Documentation Hub

Welcome to the central technical documentation repository for the **Customer Segmentation & Retention Analytics in Power BI** portfolio project. All system architectures, data models, Power Query ETL guides, DAX libraries, dashboard specifications, PBIP project definitions, and validation reports are cataloged in this directory.

---

## 📑 Technical Documentation Catalog

| Document | Purpose & Scope | Current Status |
| :--- | :--- | :---: |
| **[README.md](file:///D:/ML/Sentimental Analysis/README.md)** | Master portfolio presentation README: business context, dual-dashboard architecture, KPI definitions, setup guide, and verification matrix. | **Implemented & Verified [OK]** |
| **[powerbi/dashboard_spec.md](file:///D:/ML/Sentimental Analysis/powerbi/dashboard_spec.md)** | Full 3-page Power BI dashboard design specification, visual field mappings, visual roles, and slicer interactions. | **Implemented & Verified [OK]** |
| **[powerbi/visual_layout_guide.md](file:///D:/ML/Sentimental Analysis/powerbi/visual_layout_guide.md)** | Canvas coordinate maps ($1280 \times 720$ px), visual container dimensions, and step-by-step build sequence. | **Implemented & Verified [OK]** |
| **[powerbi/data_model.md](file:///D:/ML/Sentimental Analysis/powerbi/data_model.md)** | Single-table model specification for `CustomerData`, column typing, summarization, display formats, and Star Schema roadmap. | **Implemented & Verified [OK]** |
| **[powerbi/power_query_steps.md](file:///D:/ML/Sentimental Analysis/powerbi/power_query_steps.md)** | Complete copy-ready M code, schema validation, data quality checks, and snapshot date governance. | **Implemented & Verified [OK]** |
| **[powerbi/dax_measures.md](file:///D:/ML/Sentimental Analysis/powerbi/dax_measures.md)** | Complete copy-ready DAX measure library (17 measures), filter behaviors, benchmarks, and CLV discussion. | **Implemented & Verified [OK]** |
| **[docs/kpi_definitions.md](file:///D:/ML/Sentimental Analysis/docs/kpi_definitions.md)** | Business and technical metric catalog, mathematical formulas, benchmarks, and Power BI visual recommendations. | **Implemented & Verified [OK]** |
| **[docs/data_quality_summary.md](file:///D:/ML/Sentimental Analysis/docs/data_quality_summary.md)** | Comprehensive audit of data completeness, validity, accuracy, consistency, and anomaly resolution log. | **Implemented & Verified [OK]** |
| **[docs/dataset_spec.md](file:///D:/ML/Sentimental Analysis/docs/dataset_spec.md)** | Ground truth schema, business rules, fixed snapshot date (`2026-10-16`), and classification formulas. | **Implemented & Verified [OK]** |
| **[docs/dataset_validation_report.md](file:///D:/ML/Sentimental Analysis/docs/dataset_validation_report.md)** | Empirical validation report: 28/28 checks passed, actual segment distributions, and execution logs. | **Implemented & Verified [OK]** |
| **[docs/data_pipeline.md](file:///D:/ML/Sentimental Analysis/docs/data_pipeline.md)** | End-to-end data flow: synthetic generation $\to$ validation $\to$ Power BI Star Schema ingestion. | **Implemented & Verified [OK]** |
| **[docs/powerbi_project_audit.md](file:///D:/ML/Sentimental Analysis/docs/powerbi_project_audit.md)** | Complete 6-phase runtime and compatibility audit: PBIP schema, M partition, 17 DAX checks, and 29 visual containers. | **Audit Completed [OK]** |
| **[docs/powerbi_desktop_verification.md](file:///D:/ML/Sentimental Analysis/docs/powerbi_desktop_verification.md)** | Step-by-step manual verification and validation guide for Power BI Desktop users opening the PBIP project. | **Verification Protocol Active [OK]** |
| **[docs/architecture.md](file:///D:/ML/Sentimental Analysis/docs/architecture.md)** | Dual-dashboard technical architecture, independent pipeline design, and Mermaid system diagram. | **Implemented & Verified [OK]** |
| **[docs/validation_and_testing.md](file:///D:/ML/Sentimental Analysis/docs/validation_and_testing.md)** | Multi-tier testing protocols, sanity checks, and validation standards. | **Active** |

---

## 📁 Project Deliverables & Assets

- **Power BI Project (`.pbip`) Files:**
  - Project Pointer: [`powerbi/Customer_Segmentation_Retention.pbip`](file:///D:/ML/Sentimental%20Analysis/powerbi/Customer_Segmentation_Retention.pbip)
  - Report Definition: [`powerbi/Customer_Segmentation_Retention.Report/report.json`](file:///D:/ML/Sentimental%20Analysis/powerbi/Customer_Segmentation_Retention.Report/report.json)
  - Semantic Model: [`powerbi/Customer_Segmentation_Retention.SemanticModel/model.bim`](file:///D:/ML/Sentimental%20Analysis/powerbi/Customer_Segmentation_Retention.SemanticModel/model.bim)
  - Custom Theme: [`powerbi/theme.json`](file:///D:/ML/Sentimental%20Analysis/powerbi/theme.json)
- **Power BI Layout & Design Specs:**
  - [`powerbi/dashboard_spec.md`](file:///D:/ML/Sentimental%20Analysis/powerbi/dashboard_spec.md)
  - [`powerbi/visual_layout_guide.md`](file:///D:/ML/Sentimental%20Analysis/powerbi/visual_layout_guide.md)
  - [`powerbi/data_model.md`](file:///D:/ML/Sentimental%20Analysis/powerbi/data_model.md)
  - [`powerbi/power_query_steps.md`](file:///D:/ML/Sentimental%20Analysis/powerbi/power_query_steps.md)
  - [`powerbi/dax_measures.md`](file:///D:/ML/Sentimental%20Analysis/powerbi/dax_measures.md)
- **Data Dictionary & Raw Datasets:**
  - Data Dictionary: [`data/data_dictionary.md`](file:///D:/ML/Sentimental%20Analysis/data/data_dictionary.md)
  - Raw CSV Dataset: [`data/raw/customer_segmentation_retention_sample.csv`](file:///D:/ML/Sentimental%20Analysis/data/raw/customer_segmentation_retention_sample.csv)
  - Raw Excel Workbook: [`data/raw/customer_segmentation_retention_sample.xlsx`](file:///D:/ML/Sentimental%20Analysis/data/raw/customer_segmentation_retention_sample.xlsx)
- **Automated Validation Engines:**
  - Dataset Generator: [`scripts/generate_dataset.py`](file:///D:/ML/Sentimental%20Analysis/scripts/generate_dataset.py)
  - Dataset Validator (28 checks): [`scripts/validate_dataset.py`](file:///D:/ML/Sentimental%20Analysis/scripts/validate_dataset.py)
  - Benchmark Calculator: [`scripts/compute_metrics.py`](file:///D:/ML/Sentimental%20Analysis/scripts/compute_metrics.py)
  - DAX Math & Filter Validator (25 checks): [`scripts/validate_dax_measures.py`](file:///D:/ML/Sentimental%20Analysis/scripts/validate_dax_measures.py)
  - PBIP Structure & Dashboard Validator (15 checks): [`scripts/validate_dashboard_spec.py`](file:///D:/ML/Sentimental%20Analysis/scripts/validate_dashboard_spec.py)
  - Comprehensive Project & Runtime Auditor (31 checks): [`scripts/validate_powerbi_project.py`](file:///D:/ML/Sentimental%20Analysis/scripts/validate_powerbi_project.py)
  - Web Companion Regression Suite (15 checks): [`scripts/test_preview_functionality.py`](file:///D:/ML/Sentimental%20Analysis/scripts/test_preview_functionality.py)

---

## 🔄 Reproduction & Execution Commands

```powershell
# 1. Generate the 150-record dataset
& "D:\ML\python\python.exe" scripts/generate_dataset.py

# 2. Execute automated 28-point dataset validation suite
& "D:\ML\python\python.exe" scripts/validate_dataset.py

# 3. Calculate all empirical ground truth benchmarks
& "D:\ML\python\python.exe" scripts/compute_metrics.py

# 4. Execute automated DAX measure validation & filter simulation suite
& "D:\ML\python\python.exe" scripts/validate_dax_measures.py

# 5. Execute automated Power BI Project structure and dashboard spec validation suite
& "D:\ML\python\python.exe" scripts/validate_dashboard_spec.py

# 6. Execute comprehensive Power BI Project runtime & compatibility audit
& "D:\ML\python\python.exe" scripts/validate_powerbi_project.py

# 7. Start the live interactive web companion dashboard on localhost
& "D:\ML\python\python.exe" web/server.py
# URL: http://localhost:8080
```
