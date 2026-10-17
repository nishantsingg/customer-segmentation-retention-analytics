"""
Customer Segmentation & Retention Analytics - Comprehensive Dataset Validator
Project: Customer Segmentation & Retention Analytics in Power BI
Workspace: D:/ML/Sentimental Analysis

Validates data integrity, business logic adherence, schema compliance,
reproducibility, and CSV/Excel parity for the customer segmentation dataset.
"""

import os
import sys
import datetime
import pandas as pd
import openpyxl

SNAPSHOT_DATE = datetime.date(2026, 10, 16)
EXPECTED_RECORD_COUNT = 150
EXPECTED_COLUMNS = [
    "Customer ID",
    "Customer Name",
    "Age",
    "Gender",
    "City/Region",
    "Occupation",
    "Income Level",
    "Join Date",
    "Last Purchase Date",
    "Purchase Frequency",
    "Average Order Value",
    "Total Spend",
    "Preferred Product Category",
    "Purchase Channel",
    "Customer Type",
    "Engagement Score",
    "Satisfaction Score",
    "Retention Status",
    "Customer Segment",
    "Loyalty Tier"
]

EXPECTED_SEGMENTS = {
    "Champions",
    "Loyal Customers",
    "New / Potential Loyalist",
    "At Risk - High Value",
    "Needs Nurturing",
    "Hibernating"
}

EXPECTED_TIERS = {"Bronze", "Silver", "Gold", "Platinum"}
EXPECTED_RETENTION = {"Retained", "At Risk", "Churned"}
EXPECTED_CUSTOMER_TYPES = {"New", "Returning"}
EXPECTED_CHANNELS = {"Mobile App", "Website", "In-Store", "Omnichannel"}

class ValidationSuite:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.csv_path = os.path.join(project_root, "data", "raw", "customer_segmentation_retention_sample.csv")
        self.xlsx_path = os.path.join(project_root, "data", "raw", "customer_segmentation_retention_sample.xlsx")
        self.results = []
        self.df_csv = None
        self.df_xlsx = None

    def log_result(self, test_name: str, passed: bool, details: str):
        status_icon = "PASS" if passed else "FAIL"
        self.results.append({
            "test_name": test_name,
            "passed": passed,
            "details": details
        })
        print(f"[{status_icon:4}] {test_name}: {details}")

    def load_datasets(self) -> bool:
        print("\n--- 1. File Existence & Loading ---")
        if not os.path.exists(self.csv_path):
            self.log_result("CSV Existence", False, f"Missing file: {self.csv_path}")
            return False
        self.log_result("CSV Existence", True, f"Found: {self.csv_path}")

        if not os.path.exists(self.xlsx_path):
            self.log_result("Excel Existence", False, f"Missing file: {self.xlsx_path}")
            return False
        self.log_result("Excel Existence", True, f"Found: {self.xlsx_path}")

        try:
            self.df_csv = pd.read_csv(self.csv_path, dtype={"Customer ID": str})
            self.log_result("CSV Parsing", True, f"Parsed {len(self.df_csv)} records")
        except Exception as e:
            self.log_result("CSV Parsing", False, f"Failed parsing CSV: {str(e)}")
            return False

        try:
            wb = openpyxl.load_workbook(self.xlsx_path, read_only=True)
            sheet_names = wb.sheetnames
            expected_sheets = ["Customer Dataset", "Data Dictionary"]
            has_sheets = all(s in sheet_names for s in expected_sheets)
            self.log_result("Excel Sheet Verification", has_sheets, f"Sheets present: {sheet_names}")
            wb.close()

            self.df_xlsx = pd.read_excel(self.xlsx_path, sheet_name="Customer Dataset", dtype={"Customer ID": str})
            self.log_result("Excel Customer Dataset Parsing", True, f"Parsed {len(self.df_xlsx)} records")
        except Exception as e:
            self.log_result("Excel Customer Dataset Parsing", False, f"Failed parsing Excel: {str(e)}")
            return False

        return True

    def validate_row_and_column_counts(self):
        print("\n--- 2. Record & Column Counts ---")
        # CSV counts
        csv_rows, csv_cols = self.df_csv.shape
        self.log_result(
            "CSV Row Count",
            csv_rows == EXPECTED_RECORD_COUNT,
            f"Expected {EXPECTED_RECORD_COUNT}, got {csv_rows}"
        )
        self.log_result(
            "CSV Column Count",
            csv_cols == len(EXPECTED_COLUMNS),
            f"Expected {len(EXPECTED_COLUMNS)}, got {csv_cols}"
        )

        # Excel counts
        xlsx_rows, xlsx_cols = self.df_xlsx.shape
        self.log_result(
            "Excel Row Count",
            xlsx_rows == EXPECTED_RECORD_COUNT,
            f"Expected {EXPECTED_RECORD_COUNT}, got {xlsx_rows}"
        )
        self.log_result(
            "Excel Column Count",
            xlsx_cols == len(EXPECTED_COLUMNS),
            f"Expected {len(EXPECTED_COLUMNS)}, got {xlsx_cols}"
        )

    def validate_schema_and_column_names(self):
        print("\n--- 3. Schema & Column Names ---")
        csv_col_diff = [c for c in EXPECTED_COLUMNS if c not in self.df_csv.columns]
        self.log_result(
            "CSV Column Names",
            len(csv_col_diff) == 0,
            f"Missing columns: {csv_col_diff}" if csv_col_diff else "All 20 expected columns match exactly"
        )

        xlsx_col_diff = [c for c in EXPECTED_COLUMNS if c not in self.df_xlsx.columns]
        self.log_result(
            "Excel Column Names",
            len(xlsx_col_diff) == 0,
            f"Missing columns: {xlsx_col_diff}" if xlsx_col_diff else "All 20 expected columns match exactly"
        )

    def validate_primary_keys_and_nulls(self):
        print("\n--- 4. Primary Keys & Completeness ---")
        # Customer ID uniqueness
        unique_ids = self.df_csv["Customer ID"].nunique()
        self.log_result(
            "Customer ID Uniqueness",
            unique_ids == EXPECTED_RECORD_COUNT,
            f"{unique_ids} unique IDs for {EXPECTED_RECORD_COUNT} records"
        )

        # Non-blank IDs
        blank_ids = self.df_csv["Customer ID"].str.strip().eq("").sum()
        self.log_result("Customer ID Non-Blank", blank_ids == 0, f"Found {blank_ids} blank IDs")

        # Null value check
        total_nulls = self.df_csv.isnull().sum().sum()
        self.log_result("Zero Missing / Null Values", total_nulls == 0, f"Total null values: {total_nulls}")

    def validate_business_rules_and_calculations(self):
        print("\n--- 5. Business Rules & Logic Integrity ---")
        df = self.df_csv.copy()

        # Rule 2: Age range 18-90
        invalid_age = df[~df["Age"].between(18, 90)]
        self.log_result(
            "Rule: Age Range [18, 90]",
            len(invalid_age) == 0,
            f"Invalid age records: {len(invalid_age)}"
        )

        # Rule 3: Purchase Frequency positive integer
        invalid_freq = df[df["Purchase Frequency"] < 1]
        self.log_result(
            "Rule: Positive Purchase Frequency",
            len(invalid_freq) == 0,
            f"Non-positive frequency records: {len(invalid_freq)}"
        )

        # Rule 4: AOV nonnegative
        invalid_aov = df[df["Average Order Value"] < 0]
        self.log_result(
            "Rule: Nonnegative Average Order Value",
            len(invalid_aov) == 0,
            f"Negative AOV records: {len(invalid_aov)}"
        )

        # Rule 5: Total Spend = Purchase Frequency * Average Order Value (+/- 0.01 tolerance)
        calculated_spend = df["Purchase Frequency"] * df["Average Order Value"]
        spend_diff = (df["Total Spend"] - calculated_spend).abs()
        invalid_spend = df[spend_diff > 0.01]
        self.log_result(
            "Rule: Total Spend Math Integrity (Freq * AOV)",
            len(invalid_spend) == 0,
            f"Mismatched spend records (tolerance > 0.01): {len(invalid_spend)}"
        )

        # Dates conversion
        df["Join Date Obj"] = pd.to_datetime(df["Join Date"]).dt.date
        df["Last Purchase Date Obj"] = pd.to_datetime(df["Last Purchase Date"]).dt.date

        # Rule 6: Last Purchase Date <= Snapshot Date
        future_purchases = df[df["Last Purchase Date Obj"] > SNAPSHOT_DATE]
        self.log_result(
            "Rule: Last Purchase Date <= Snapshot Date (2026-10-16)",
            len(future_purchases) == 0,
            f"Purchases after snapshot: {len(future_purchases)}"
        )

        # Rule 7: Join Date <= Last Purchase Date
        invalid_join = df[df["Join Date Obj"] > df["Last Purchase Date Obj"]]
        self.log_result(
            "Rule: Join Date <= Last Purchase Date",
            len(invalid_join) == 0,
            f"Join date after last purchase records: {len(invalid_join)}"
        )

        # Rule 8: Customer Type (New when Freq == 1, else Returning)
        expected_type = df["Purchase Frequency"].apply(lambda f: "New" if f == 1 else "Returning")
        mismatched_type = df[df["Customer Type"] != expected_type]
        self.log_result(
            "Rule: Customer Type Calculation",
            len(mismatched_type) == 0,
            f"Mismatched customer type records: {len(mismatched_type)}"
        )

        # Rule 9: Retention Status
        days_since_purchase = (SNAPSHOT_DATE - df["Last Purchase Date Obj"]).apply(lambda d: d.days)
        expected_retention = days_since_purchase.apply(
            lambda days: "Retained" if days <= 60 else ("At Risk" if days <= 150 else "Churned")
        )
        mismatched_retention = df[df["Retention Status"] != expected_retention]
        self.log_result(
            "Rule: Retention Status Calculation (Recency Brackets)",
            len(mismatched_retention) == 0,
            f"Mismatched retention status records: {len(mismatched_retention)}"
        )

        # Rule 10: Loyalty Tier
        def get_tier(spend):
            if spend < 15000.0:
                return "Bronze"
            elif spend < 40000.0:
                return "Silver"
            elif spend < 80000.0:
                return "Gold"
            else:
                return "Platinum"

        expected_tier = df["Total Spend"].apply(get_tier)
        mismatched_tier = df[df["Loyalty Tier"] != expected_tier]
        self.log_result(
            "Rule: Loyalty Tier Calculation (Spend Brackets)",
            len(mismatched_tier) == 0,
            f"Mismatched loyalty tier records: {len(mismatched_tier)}"
        )

        # Rule 11: Customer Segment mutually exclusive & deterministic
        def get_segment(row):
            status = row["Retention Status"]
            tier = row["Loyalty Tier"]
            freq = row["Purchase Frequency"]
            c_type = row["Customer Type"]
            if status == "Retained":
                if tier in ["Gold", "Platinum"] and freq >= 5:
                    return "Champions"
                elif tier in ["Silver", "Gold", "Platinum"]:
                    return "Loyal Customers"
                else:
                    return "New / Potential Loyalist"
            elif status == "At Risk":
                if tier in ["Gold", "Platinum"]:
                    return "At Risk - High Value"
                elif c_type == "New":
                    return "New / Potential Loyalist"
                else:
                    return "Needs Nurturing"
            else:  # Churned
                if tier in ["Gold", "Platinum"]:
                    return "At Risk - High Value"
                else:
                    return "Hibernating"

        expected_segment = df.apply(get_segment, axis=1)
        mismatched_segment = df[df["Customer Segment"] != expected_segment]
        self.log_result(
            "Rule: Customer Segment Calculation (Deterministic & Exclusive)",
            len(mismatched_segment) == 0,
            f"Mismatched customer segment records: {len(mismatched_segment)}"
        )

        # Rule 12: Score ranges
        invalid_engagement = df[~df["Engagement Score"].between(1, 100)]
        self.log_result(
            "Rule: Engagement Score Range [1, 100]",
            len(invalid_engagement) == 0,
            f"Invalid engagement score records: {len(invalid_engagement)}"
        )

        invalid_csat = df[~df["Satisfaction Score"].between(1.0, 5.0)]
        self.log_result(
            "Rule: Satisfaction Score Range [1.0, 5.0]",
            len(invalid_csat) == 0,
            f"Invalid satisfaction score records: {len(invalid_csat)}"
        )

    def validate_csv_excel_consistency(self):
        print("\n--- 6. CSV vs Excel Data Consistency ---")
        df_c = self.df_csv.copy()
        df_x = self.df_xlsx.copy()

        # Convert dates to string representation
        df_c["Join Date"] = pd.to_datetime(df_c["Join Date"]).dt.strftime("%Y-%m-%d")
        df_c["Last Purchase Date"] = pd.to_datetime(df_c["Last Purchase Date"]).dt.strftime("%Y-%m-%d")
        df_x["Join Date"] = pd.to_datetime(df_x["Join Date"]).dt.strftime("%Y-%m-%d")
        df_x["Last Purchase Date"] = pd.to_datetime(df_x["Last Purchase Date"]).dt.strftime("%Y-%m-%d")

        # Compare column by column
        mismatches = []
        for col in EXPECTED_COLUMNS:
            if col in ["Average Order Value", "Total Spend", "Satisfaction Score"]:
                diff = (df_c[col] - df_x[col]).abs().max()
                if diff > 0.001:
                    mismatches.append(f"{col} float delta ({diff})")
            else:
                mismatch_count = (df_c[col].astype(str) != df_x[col].astype(str)).sum()
                if mismatch_count > 0:
                    mismatches.append(f"{col} ({mismatch_count} differences)")

        self.log_result(
            "CSV vs Excel Parity",
            len(mismatches) == 0,
            "100% cell-by-cell match across all 150 rows" if not mismatches else f"Differences in: {mismatches}"
        )

    def validate_reproducibility(self):
        print("\n--- 7. Generator Determinism & Reproducibility ---")
        try:
            if self.project_root not in sys.path:
                sys.path.insert(0, self.project_root)
            from scripts.generate_dataset import generate_dataset
            df_run1 = generate_dataset(seed=42)
            df_run2 = generate_dataset(seed=42)

            is_identical = df_run1.equals(df_run2)
            self.log_result(
                "Seed Reproducibility",
                is_identical,
                "Independent re-runs with seed=42 yield bit-for-bit identical DataFrames"
            )
        except Exception as e:
            self.log_result("Seed Reproducibility", False, f"Error testing reproducibility: {str(e)}")

    def print_distribution_summary(self):
        print("\n=======================================================")
        print("          DATASET SEGMENTATION BREAKDOWN               ")
        print("=======================================================")
        print("\n1. Retention Status Counts:")
        retention_counts = self.df_csv["Retention Status"].value_counts()
        for k, v in retention_counts.items():
            print(f"   - {k:15}: {v:3} ({v / len(self.df_csv):.1%})")

        print("\n2. Customer Segment Counts:")
        segment_counts = self.df_csv["Customer Segment"].value_counts()
        for k, v in segment_counts.items():
            print(f"   - {k:25}: {v:3} ({v / len(self.df_csv):.1%})")

        print("\n3. Loyalty Tier Counts:")
        tier_counts = self.df_csv["Loyalty Tier"].value_counts()
        for k, v in tier_counts.items():
            print(f"   - {k:15}: {v:3} ({v / len(self.df_csv):.1%})")

        print("\n4. Customer Type Counts:")
        type_counts = self.df_csv["Customer Type"].value_counts()
        for k, v in type_counts.items():
            print(f"   - {k:15}: {v:3} ({v / len(self.df_csv):.1%})")

    def run_all(self) -> bool:
        if not self.load_datasets():
            return False
        self.validate_row_and_column_counts()
        self.validate_schema_and_column_names()
        self.validate_primary_keys_and_nulls()
        self.validate_business_rules_and_calculations()
        self.validate_csv_excel_consistency()
        self.validate_reproducibility()
        self.print_distribution_summary()

        all_passed = all(r["passed"] for r in self.results)
        print("\n=======================================================")
        print(f"VALIDATION SUMMARY: {'ALL CHECKS PASSED [OK]' if all_passed else 'SOME CHECKS FAILED [FAIL]'}")
        print(f"Passed: {sum(1 for r in self.results if r['passed'])} / {len(self.results)}")
        print("=======================================================\n")
        return all_passed

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    suite = ValidationSuite(project_root)
    success = suite.run_all()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
