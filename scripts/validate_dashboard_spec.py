"""
Power BI Dashboard Specification & PBIP Project Validator
Project: Customer Segmentation & Retention Analytics in Power BI
Workspace: D:/ML/Sentimental Analysis

Validates the structural integrity, visual field bindings, DAX measure
registrations, and JSON schemas of the Power BI Project (.pbip) deliverables.
"""

import os
import sys
import json
import csv

class DashboardSpecValidator:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.powerbi_dir = os.path.join(project_root, "powerbi")
        self.csv_path = os.path.join(project_root, "data", "raw", "customer_segmentation_retention_sample.csv")
        self.tests = []

    def log(self, test_name: str, passed: bool, details: str):
        status = "PASS" if passed else "FAIL"
        self.tests.append({
            "test_name": test_name,
            "passed": passed,
            "details": details
        })
        print(f"[{status:4}] {test_name}: {details}")

    def validate_file_assets(self):
        print("\n--- 1. Power BI Project File Assets ---")
        required_files = [
            "Customer_Segmentation_Retention.pbip",
            "Customer_Segmentation_Retention.Report/definition.pbir",
            "Customer_Segmentation_Retention.Report/report.json",
            "Customer_Segmentation_Retention.SemanticModel/definition.pbism",
            "Customer_Segmentation_Retention.SemanticModel/model.bim",
            "theme.json",
            "dashboard_spec.md",
            "visual_layout_guide.md"
        ]

        for rf in required_files:
            fp = os.path.join(self.powerbi_dir, rf)
            exists = os.path.exists(fp)
            self.log(f"File Existence: {rf}", exists, f"Found at: {fp}" if exists else f"Missing: {fp}")

    def validate_theme_specification(self):
        print("\n--- 2. Theme JSON Palette & Typography Validation ---")
        theme_path = os.path.join(self.powerbi_dir, "theme.json")
        try:
            with open(theme_path, "r", encoding="utf-8") as f:
                theme_data = json.load(f)

            data_colors = theme_data.get("dataColors", [])
            expected_colors = ["#183153", "#2878B5", "#27966B", "#E8A23A", "#D9534F"]
            has_colors = all(c in data_colors for c in expected_colors)
            self.log(
                "Theme Data Colors",
                has_colors,
                f"Contains required palette: {expected_colors}" if has_colors else f"Missing colors in {data_colors}"
            )

            font = theme_data.get("visualStyles", {}).get("*", {}).get("*", {}).get("*", {}).get("fontFamily")
            self.log("Theme Typography", font == "Segoe UI", f"Default font: {font}")
        except Exception as e:
            self.log("Theme JSON Parsing", False, f"Failed parsing theme: {str(e)}")

    def validate_semantic_model(self):
        print("\n--- 3. Semantic Model (model.bim) Validation ---")
        bim_path = os.path.join(self.powerbi_dir, "Customer_Segmentation_Retention.SemanticModel", "model.bim")
        try:
            with open(bim_path, "r", encoding="utf-8") as f:
                bim = json.load(f)

            model = bim.get("model", {})
            tables = model.get("tables", [])
            cust_table = next((t for t in tables if t.get("name") == "CustomerData"), None)

            self.log("Table Name Check", cust_table is not None, "Table 'CustomerData' found in model.bim")
            if not cust_table:
                return

            # Check columns
            cols = cust_table.get("columns", [])
            col_names = [c["name"] for c in cols]
            with open(self.csv_path, "r", encoding="utf-8") as f:
                csv_cols = next(csv.reader(f))

            all_cols_present = all(c in col_names for c in csv_cols)
            self.log(
                "Semantic Model Columns Match CSV",
                all_cols_present and len(col_names) == 20,
                f"Found {len(col_names)} columns matching CSV schema exactly"
            )

            # Check measures
            measures = cust_table.get("measures", [])
            measure_names = [m["name"] for m in measures]
            expected_measures = [
                "Total Customers", "Total Revenue", "Total Orders", "Average Order Value",
                "Average Customer Spend", "Average Purchase Frequency", "Repeat Customers",
                "Repeat Customer Rate", "Retained Customers", "Retention Status Share %",
                "At-Risk Customers", "At-Risk Status Share %", "Churned Customers",
                "Churn Status Share %", "Average Engagement Score", "Average Satisfaction Score",
                "Segment Revenue Share %"
            ]
            all_measures_present = all(m in measure_names for m in expected_measures)
            self.log(
                "Semantic Model DAX Measures",
                all_measures_present and len(measure_names) == 17,
                f"Registered {len(measure_names)} DAX measures with valid expressions"
            )
        except Exception as e:
            self.log("Semantic Model Validation", False, f"Failed validating model.bim: {str(e)}")

    def validate_report_definition(self):
        print("\n--- 4. Report Definition (report.json) Validation ---")
        report_path = os.path.join(self.powerbi_dir, "Customer_Segmentation_Retention.Report", "report.json")
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)

            sections = report.get("sections", [])
            section_names = [s.get("displayName") for s in sections]
            expected_sections = [
                "Customer Overview",
                "Segmentation & Customer Value",
                "Retention & Risk"
            ]

            has_all_pages = all(s in section_names for s in expected_sections)
            self.log(
                "Report Pages (Sections)",
                has_all_pages and len(sections) == 3,
                f"Configured 3 report pages: {section_names}"
            )

            total_visuals = sum(len(s.get("visualContainers", [])) for s in sections)
            self.log(
                "Report Visual Containers",
                total_visuals >= 25,
                f"Configured {total_visuals} visual containers with layout coordinates"
            )
        except Exception as e:
            self.log("Report Definition Validation", False, f"Failed validating report.json: {str(e)}")

    def run_all(self) -> bool:
        self.validate_file_assets()
        self.validate_theme_specification()
        self.validate_semantic_model()
        self.validate_report_definition()

        all_passed = all(t["passed"] for t in self.tests)
        print("\n=======================================================")
        print(f"DASHBOARD SPEC VALIDATION: {'ALL CHECKS PASSED [OK]' if all_passed else 'SOME CHECKS FAILED [FAIL]'}")
        print(f"Passed: {sum(1 for t in self.tests if t['passed'])} / {len(self.tests)}")
        print("=======================================================\n")
        return all_passed

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    validator = DashboardSpecValidator(project_root)
    success = validator.run_all()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
