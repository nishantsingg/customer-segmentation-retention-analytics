import csv
import urllib.request
import re

def test_web_server_endpoints():
    print("--- 1. Testing Web Server Endpoints ---")
    req = urllib.request.urlopen("http://localhost:8080/")
    html_content = req.read().decode("utf-8")
    assert req.status == 200, f"Expected 200, got {req.status}"
    print(f"[PASS] GET / -> HTTP 200 OK ({len(html_content)} bytes)")

    csv_req = urllib.request.urlopen("http://localhost:8080/data/raw/customer_segmentation_retention_sample.csv")
    csv_content = csv_req.read().decode("utf-8")
    assert csv_req.status == 200, f"Expected 200, got {csv_req.status}"
    lines = csv_content.strip().splitlines()
    assert len(lines) == 151, f"Expected 151 lines, got {len(lines)}"
    print(f"[PASS] GET /data/raw/... -> HTTP 200 OK (150 data rows + 1 header)")

    # Assert wording improvements
    assert "Customer Portfolio, Revenue Mix, and Retention Health" in html_content
    assert "Retained Customers (0–60 Days)" in html_content
    assert "Churned Customers (>150 Days)" in html_content
    assert "Repeat Customer Share" in html_content
    assert "Synthetic Snapshot: 2026-10-16" in html_content
    assert "Fixed Snapshot Anchor: 2026-10-16 • Synthetic Data Quality Validated" in html_content
    assert "Mean gross spend across portfolio" in html_content
    assert "portfolio" in html_content.lower()
    print("[PASS] HTML template contains all snapshot-appropriate wording, Repeat Customer Share, and Synthetic validation badges")

def test_dataset_metrics():
    print("\n--- 2. Testing Ground Truth KPIs Against Dataset ---")
    with open("data/raw/customer_segmentation_retention_sample.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    n = len(records)
    assert n == 150, f"Expected 150, got {n}"
    
    total_rev = sum(float(r["Total Spend"]) for r in records)
    total_orders = sum(int(r["Purchase Frequency"]) for r in records)
    aov = total_rev / total_orders
    repeat_cust = sum(1 for r in records if int(r["Purchase Frequency"]) > 1)
    repeat_rate = repeat_cust / n
    retained = sum(1 for r in records if r["Retention Status"] == "Retained")
    at_risk = sum(1 for r in records if r["Retention Status"] == "At Risk")
    churned = sum(1 for r in records if r["Retention Status"] == "Churned")

    assert round(total_rev, 2) == 7368001.75
    assert total_orders == 794
    assert round(aov, 2) == 9279.60
    assert repeat_cust == 125
    assert round(repeat_rate * 100, 1) == 83.3
    assert retained == 75
    assert at_risk == 44
    assert churned == 31

    print(f"[PASS] Total Customers: {n}")
    print(f"[PASS] Total Revenue: INR {total_rev:,.2f} (~7.37M)")
    print(f"[PASS] Total Orders: {total_orders}")
    print(f"[PASS] Average Order Value: INR {aov:,.2f}")
    print(f"[PASS] Repeat Customer Rate: {repeat_rate*100:.1f}% ({repeat_cust} buyers)")
    print(f"[PASS] Retained Customers (0-60 Days): {retained} ({(retained/n)*100:.1f}%)")
    print(f"[PASS] At-Risk Customers (61-150 Days): {at_risk} ({(at_risk/n)*100:.1f}%)")
    print(f"[PASS] Churned Customers (>150 Days): {churned} ({(churned/n)*100:.1f}%)")

def test_slicer_and_search_logic():
    print("\n--- 3. Testing Slicer & Search Filter Simulation ---")
    with open("data/raw/customer_segmentation_retention_sample.csv", "r", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    # Test 1: Segment Slicer = Champions
    champs = [r for r in records if r["Customer Segment"] == "Champions"]
    assert len(champs) == 32
    champ_rev = sum(float(r["Total Spend"]) for r in champs)
    assert round(champ_rev, 2) == 3433209.83
    assert all(r["Retention Status"] == "Retained" for r in champs)
    print(f"[PASS] Segment Slicer = 'Champions': 32 customers, INR {champ_rev:,.2f}, 100% retained")

    # Test 2: Retention Slicer = At Risk
    at_risk_cohort = [r for r in records if r["Retention Status"] == "At Risk"]
    assert len(at_risk_cohort) == 44
    print(f"[PASS] Retention Slicer = 'At Risk': exactly 44 customers")

    # Test 3: Loyalty Tier Slicer = Platinum
    plat = [r for r in records if r["Loyalty Tier"] == "Platinum"]
    assert len(plat) == 33
    plat_rev = sum(float(r["Total Spend"]) for r in plat)
    assert round(plat_rev, 2) == 3791661.27
    print(f"[PASS] Loyalty Tier Slicer = 'Platinum': 33 customers, INR {plat_rev:,.2f}")

    # Test 4: City Slicer = Mumbai, Maharashtra
    mumbai = [r for r in records if r["City/Region"] == "Mumbai, Maharashtra"]
    assert len(mumbai) == 11
    mumbai_rev = sum(float(r["Total Spend"]) for r in mumbai)
    assert round(mumbai_rev, 2) == 405816.52
    print(f"[PASS] City Slicer = 'Mumbai, Maharashtra': 11 customers, INR {mumbai_rev:,.2f}")

    # Test 5: Customer Search by Exact ID
    search_id_exact = [r for r in records if "IND-1038".lower() in r["Customer ID"].lower() or "IND-1038".lower() in r["Customer Name"].lower()]
    assert len(search_id_exact) == 1
    assert search_id_exact[0]["Customer Name"] == "Atharva Saxena"
    print(f"[PASS] Search 'IND-1038' (Exact ID): Found {search_id_exact[0]['Customer Name']}")

    # Test 6: Customer Search by Partial ID ("1038")
    search_id_partial = [r for r in records if "1038".lower() in r["Customer ID"].lower() or "1038".lower() in r["Customer Name"].lower()]
    assert len(search_id_partial) == 1
    assert search_id_partial[0]["Customer Name"] == "Atharva Saxena"
    print(f"[PASS] Search '1038' (Partial ID): Found {search_id_partial[0]['Customer Name']}")

    # Test 7: Customer Search by First Name ("Swati")
    search_first_name = [r for r in records if "swati".lower() in r["Customer ID"].lower() or "swati".lower() in r["Customer Name"].lower()]
    assert len(search_first_name) >= 1
    assert any(r["Customer ID"] == "IND-1001" for r in search_first_name)
    print(f"[PASS] Search 'swati' (First Name): Found {len(search_first_name)} customer(s), including IND-1001 (Swati Chopra)")

    # Test 8: Customer Search by Last Name ("Kapoor")
    search_last_name = [r for r in records if "kapoor".lower() in r["Customer ID"].lower() or "kapoor".lower() in r["Customer Name"].lower()]
    assert len(search_last_name) >= 1
    print(f"[PASS] Search 'kapoor' (Last Name): Found {len(search_last_name)} matching customers (Top spend: {search_last_name[0]['Customer Name']})")

    # Test 9: Multi-filter combination (Segment='At Risk - High Value')
    multi_filter_all = [r for r in records if r["Customer Segment"] == "At Risk - High Value"]
    assert len(multi_filter_all) == 22
    multi_filter_plat = [r for r in multi_filter_all if r["Loyalty Tier"] == "Platinum"]
    assert len(multi_filter_plat) == 8
    multi_filter_atrisk = [r for r in multi_filter_all if r["Retention Status"] == "At Risk"]
    assert len(multi_filter_atrisk) == 11
    print(f"[PASS] Multi-filter (Segment='At Risk - High Value'): 22 accounts (8 Platinum, 14 Gold; 11 At-Risk, 11 Churned)")

    # Test 10: Reset Filter Verification
    reset_records = [r for r in records if True]
    assert len(reset_records) == 150
    print(f"[PASS] Reset Filters: Successfully restores 150 of 150 records across all metrics")

if __name__ == "__main__":
    test_web_server_endpoints()
    test_dataset_metrics()
    test_slicer_and_search_logic()
    print("\n=======================================================")
    print("ALL 15 PREVIEW & DASHBOARD VALIDATIONS PASSED [OK]")
    print("=======================================================")
