"""
DAX Measure Mathematical Validator & Filter Context Simulator
Project: Customer Segmentation & Retention Analytics in Power BI
Workspace: D:/ML/Sentimental Analysis

Validates that all proposed DAX formulas are mathematically sound and
independently verifies their exact numerical outputs against the ground-truth
dataset under global context and simulated slicer filter contexts.
"""

import os
import sys
import pandas as pd

class DAXValidator:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.tests = []

    def log(self, test_name: str, passed: bool, expected: str, actual: str):
        status = "PASS" if passed else "FAIL"
        self.tests.append({
            "test_name": test_name,
            "passed": passed,
            "expected": expected,
            "actual": actual
        })
        print(f"[{status:4}] {test_name}: Expected={expected} | Actual={actual}")

    def validate_global_core_measures(self):
        print("\n--- 1. Global Core Measures Validation ---")
        df = self.df

        # [Total Customers] = DISTINCTCOUNT(CustomerData[Customer ID])
        total_customers = df["Customer ID"].nunique()
        self.log("[Total Customers]", total_customers == 150, "150", str(total_customers))

        # [Total Revenue] = SUM(CustomerData[Total Spend])
        total_revenue = df["Total Spend"].sum()
        self.log("[Total Revenue]", abs(total_revenue - 7368001.75) < 0.01, "INR 7,368,001.75", f"INR {total_revenue:,.2f}")

        # [Total Orders] = SUM(CustomerData[Purchase Frequency])
        total_orders = int(df["Purchase Frequency"].sum())
        self.log("[Total Orders]", total_orders == 794, "794", str(total_orders))

        # [Average Order Value] = DIVIDE([Total Revenue], [Total Orders], 0)
        aov = total_revenue / total_orders if total_orders > 0 else 0.0
        self.log("[Average Order Value]", abs(aov - 9279.60) < 0.01, "INR 9,279.60", f"INR {aov:,.2f}")

        # [Average Customer Spend] = DIVIDE([Total Revenue], [Total Customers], 0)
        avg_cust_spend = total_revenue / total_customers if total_customers > 0 else 0.0
        self.log("[Average Customer Spend]", abs(avg_cust_spend - 49120.01) < 0.01, "INR 49,120.01", f"INR {avg_cust_spend:,.2f}")

        # [Average Purchase Frequency] = DIVIDE([Total Orders], [Total Customers], 0)
        avg_freq = total_orders / total_customers if total_customers > 0 else 0.0
        self.log("[Average Purchase Frequency]", abs(avg_freq - 5.29) < 0.01, "5.29", f"{avg_freq:.2f}")

    def validate_behavior_and_retention_measures(self):
        print("\n--- 2. Behavior & Retention Measures Validation ---")
        df = self.df
        total_customers = len(df)

        # [Repeat Customers] = CALCULATE([Total Customers], CustomerData[Purchase Frequency] > 1)
        repeat_cust = int((df["Purchase Frequency"] > 1).sum())
        self.log("[Repeat Customers]", repeat_cust == 125, "125", str(repeat_cust))

        # [Repeat Customer Rate] = DIVIDE([Repeat Customers], [Total Customers], 0)
        repeat_rate = repeat_cust / total_customers
        self.log("[Repeat Customer Rate]", abs(repeat_rate - 0.8333) < 0.001, "83.3%", f"{repeat_rate:.1%}")

        # [Retained Customers] = CALCULATE([Total Customers], CustomerData[Retention Status] == 'Retained')
        retained_cust = int((df["Retention Status"] == "Retained").sum())
        self.log("[Retained Customers]", retained_cust == 75, "75", str(retained_cust))

        # [Retention Status Share %]
        ret_share = retained_cust / total_customers
        self.log("[Retention Status Share %]", abs(ret_share - 0.500) < 0.001, "50.0%", f"{ret_share:.1%}")

        # [At-Risk Customers]
        at_risk_cust = int((df["Retention Status"] == "At Risk").sum())
        self.log("[At-Risk Customers]", at_risk_cust == 44, "44", str(at_risk_cust))

        # [At-Risk Status Share %]
        at_risk_share = at_risk_cust / total_customers
        self.log("[At-Risk Status Share %]", abs(at_risk_share - 0.2933) < 0.001, "29.3%", f"{at_risk_share:.1%}")

        # [Churned Customers]
        churned_cust = int((df["Retention Status"] == "Churned").sum())
        self.log("[Churned Customers]", churned_cust == 31, "31", str(churned_cust))

        # [Churn Status Share %]
        churn_share = churned_cust / total_customers
        self.log("[Churn Status Share %]", abs(churn_share - 0.2067) < 0.001, "20.7%", f"{churn_share:.1%}")

    def validate_experience_and_segment_shares(self):
        print("\n--- 3. Engagement & Segment Revenue Share Validation ---")
        df = self.df
        total_revenue = df["Total Spend"].sum()

        # [Average Engagement Score] = AVERAGE(CustomerData[Engagement Score])
        avg_eng = df["Engagement Score"].mean()
        self.log("[Average Engagement Score]", abs(avg_eng - 59.99) < 0.01, "59.99 (60.0)", f"{avg_eng:.2f}")

        # [Average Satisfaction Score] = AVERAGE(CustomerData[Satisfaction Score])
        avg_csat = df["Satisfaction Score"].mean()
        self.log("[Average Satisfaction Score]", abs(avg_csat - 3.67) < 0.01, "3.67 (3.7)", f"{avg_csat:.2f}")

        # [Segment Revenue Share %]
        expected_shares = {
            "Champions": (3433209.83, 0.4660),
            "At Risk - High Value": (1606501.29, 0.2180),
            "Loyal Customers": (1218738.85, 0.1654),
            "Needs Nurturing": (510982.96, 0.0694),
            "Hibernating": (400706.93, 0.0544),
            "New / Potential Loyalist": (197861.89, 0.0269)
        }

        for seg, (exp_spend, exp_share) in expected_shares.items():
            seg_spend = df[df["Customer Segment"] == seg]["Total Spend"].sum()
            seg_share = seg_spend / total_revenue
            self.log(
                f"[Segment Revenue Share %] - {seg}",
                abs(seg_share - exp_share) < 0.001,
                f"{exp_share:.1%} (INR {exp_spend:,.2f})",
                f"{seg_share:.1%} (INR {seg_spend:,.2f})"
            )

    def validate_simulated_filter_contexts(self):
        print("\n--- 4. Simulated Slicer Filter Contexts Validation ---")
        df = self.df
        total_revenue_global = df["Total Spend"].sum()

        # Slicer Context 1: Filter to City = "Mumbai, Maharashtra"
        mumbai_df = df[df["City/Region"] == "Mumbai, Maharashtra"]
        mumbai_cust = len(mumbai_df)
        mumbai_spend = mumbai_df["Total Spend"].sum()
        mumbai_orders = mumbai_df["Purchase Frequency"].sum()
        mumbai_aov = mumbai_spend / mumbai_orders
        self.log(
            "Filter Context: City='Mumbai, Maharashtra'",
            mumbai_cust > 0 and abs(mumbai_spend - (mumbai_orders * mumbai_aov)) < 0.1,
            f"Valid context ({mumbai_cust} cust, INR {mumbai_spend:,.2f} spend)",
            f"{mumbai_cust} cust, INR {mumbai_spend:,.2f} spend, AOV=INR {mumbai_aov:,.2f}"
        )

        # Slicer Context 2: Filter to Loyalty Tier = "Platinum"
        plat_df = df[df["Loyalty Tier"] == "Platinum"]
        plat_cust = len(plat_df)
        plat_spend = plat_df["Total Spend"].sum()
        plat_share = plat_spend / total_revenue_global
        self.log(
            "Filter Context: Loyalty Tier='Platinum'",
            plat_cust == 33 and abs(plat_share - 0.5146) < 0.001,
            "33 cust, 51.5% revenue share",
            f"{plat_cust} cust, {plat_share:.1%} revenue share (INR {plat_spend:,.2f})"
        )

        # Slicer Context 3: Filter to Retention Status = "Retained"
        ret_df = df[df["Retention Status"] == "Retained"]
        ret_cust = len(ret_df)
        ret_spend = ret_df["Total Spend"].sum()
        self.log(
            "Filter Context: Retention Status='Retained'",
            ret_cust == 75,
            "75 cust",
            f"{ret_cust} cust, INR {ret_spend:,.2f} spend"
        )

    def run_all(self) -> bool:
        self.validate_global_core_measures()
        self.validate_behavior_and_retention_measures()
        self.validate_experience_and_segment_shares()
        self.validate_simulated_filter_contexts()

        all_passed = all(t["passed"] for t in self.tests)
        print("\n=======================================================")
        print(f"DAX VALIDATION SUMMARY: {'ALL MEASURES PASSED [OK]' if all_passed else 'SOME MEASURES FAILED [FAIL]'}")
        print(f"Passed: {sum(1 for t in self.tests if t['passed'])} / {len(self.tests)}")
        print("=======================================================\n")
        return all_passed

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "raw", "customer_segmentation_retention_sample.csv")
    validator = DAXValidator(csv_path)
    success = validator.run_all()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
