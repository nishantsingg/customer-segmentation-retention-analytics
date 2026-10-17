"""
PBIP Portability & Visual Readability Enhancer
Project: Customer Segmentation & Retention Analytics in Power BI
Workspace: D:/ML/Sentimental Analysis

1. Adds a native Power Query parameter 'DatasetFilePath' to model.bim.
2. Updates CustomerData partition M expression to use DatasetFilePath.
3. Enhances Page 2 Loyalty Tier visual in report.json to use a dual-axis
   lineClusteredColumnChart so both Total Revenue (bars) and Customer Count (line)
   are clearly interpretable without scaling distortion.
"""

import os
import json

def update_model_portability(project_root: str):
    bim_path = os.path.join(project_root, "powerbi", "Customer_Segmentation_Retention.SemanticModel", "model.bim")
    with open(bim_path, "r", encoding="utf-8") as f:
        bim = json.load(f)

    # 1. Add model-level parameter expression
    bim["model"]["expressions"] = [
        {
            "name": "DatasetFilePath",
            "kind": "m",
            "expression": [
                '"D:\\\\ML\\\\Sentimental Analysis\\\\data\\\\raw\\\\customer_segmentation_retention_sample.csv" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'
            ],
            "description": "Configurable file path for the raw customer segmentation dataset. Update via Home > Transform Data > Edit Parameters in Power BI Desktop."
        }
    ]

    # 2. Update CustomerData partition M query
    partition_m = [
        "let",
        "    // Ingest dataset using configurable parameter DatasetFilePath",
        "    SourceFilePath = DatasetFilePath,",
        '    Source = Csv.Document(File.Contents(SourceFilePath), [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        "    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
        "    TypedTable = Table.TransformColumnTypes(PromotedHeaders, {",
        '        {"Customer ID", type text}, {"Customer Name", type text}, {"Age", Int64.Type},',
        '        {"Gender", type text}, {"City/Region", type text}, {"Occupation", type text},',
        '        {"Income Level", type text}, {"Join Date", type date}, {"Last Purchase Date", type date},',
        '        {"Purchase Frequency", Int64.Type}, {"Average Order Value", type number},',
        '        {"Total Spend", type number}, {"Preferred Product Category", type text},',
        '        {"Purchase Channel", type text}, {"Customer Type", type text},',
        '        {"Engagement Score", Int64.Type}, {"Satisfaction Score", type number},',
        '        {"Retention Status", type text}, {"Customer Segment", type text},',
        '        {"Loyalty Tier", type text}',
        "    }),",
        '    CleanedRows = Table.SelectRows(TypedTable, each [Customer ID] <> null and [Customer ID] <> "")',
        "in",
        "    CleanedRows"
    ]

    bim["model"]["tables"][0]["partitions"][0]["source"]["expression"] = partition_m

    with open(bim_path, "w", encoding="utf-8") as f:
        json.dump(bim, f, indent=2)

    print("[OK] Successfully updated model.bim with DatasetFilePath parameter.")

def update_visual_readability(project_root: str):
    report_path = os.path.join(project_root, "powerbi", "Customer_Segmentation_Retention.Report", "report.json")
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    # In Section 2 (Segmentation & Customer Value), find Chart_LoyaltyTierComparison
    sec2 = report["sections"][1]
    for container in sec2["visualContainers"]:
        cfg_str = container.get("config", "{}")
        cfg = json.loads(cfg_str)
        if cfg.get("name") == "Chart_LoyaltyTierComparison":
            # Redesign as lineClusteredColumnChart with dual axis:
            # Columns (Y) = Total Revenue
            # Line (Y2) = Total Customers
            cfg["singleVisual"]["visualType"] = "lineClusteredColumnChart"
            cfg["singleVisual"]["projections"] = {
                "Category": [{"queryRef": "CustomerData.Loyalty Tier"}],
                "Y": [{"queryRef": "CustomerData.Total Revenue"}],
                "Y2": [{"queryRef": "CustomerData.Total Customers"}]
            }
            cfg["singleVisual"]["vcObjects"] = {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"literal": {"value": "true"}}},
                            "text": {"expr": {"literal": {"value": "Total Revenue (Bars) & Customer Count (Line) by Loyalty Tier"}}}
                        }
                    }
                ]
            }
            container["config"] = json.dumps(cfg)
            print("[OK] Successfully upgraded Chart_LoyaltyTierComparison to lineClusteredColumnChart (Dual-Axis).")
            break

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    update_model_portability(project_root)
    update_visual_readability(project_root)
    print("All portability and readability updates applied!")

if __name__ == "__main__":
    main()
