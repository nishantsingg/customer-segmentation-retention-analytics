/**
 * Customer Segmentation & Retention Analytics
 * Interactive Power BI Web Companion Engine
 */

let allCustomers = [];
let filteredCustomers = [];
let sortCol = "Total Spend";
let sortAsc = false;
let quickStatusFilter = "ALL";

// Chart instances dictionary
const charts = {};

// Palette
const PALETTE = {
  navy: "#183153",
  blue: "#2878b5",
  cyan: "#38bdf8",
  green: "#27966b",
  amber: "#e8a23a",
  red: "#d9534f",
  purple: "#a78bfa",
  series: ["#2878b5", "#38bdf8", "#27966b", "#e8a23a", "#a78bfa", "#f43f5e", "#94a3b8"]
};

// Formatting helpers
function formatINR(val, compact = false) {
  if (isNaN(val) || val === null) return "₹0.00";
  if (compact) {
    if (Math.abs(val) >= 1e7) return "₹" + (val / 1e7).toFixed(2) + " Cr";
    if (Math.abs(val) >= 1e6) return "₹" + (val / 1e6).toFixed(2) + "M";
    if (Math.abs(val) >= 1e5) return "₹" + (val / 1e5).toFixed(2) + " Lakh";
    if (Math.abs(val) >= 1e3) return "₹" + (val / 1e3).toFixed(1) + "k";
  }
  return "₹" + Number(val).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatPercent(val) {
  if (isNaN(val) || val === null) return "0.0%";
  return (val * 100).toFixed(1) + "%";
}

// Parse CSV text with quote support
function parseCSV(text) {
  const lines = text.trim().split(/\r?\n/);
  if (lines.length < 2) return [];
  const headers = lines[0].split(",").map(h => h.trim().replace(/^"|"$/g, ''));
  const rows = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    
    // Regex to split comma while preserving quoted strings
    const match = line.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g) || line.split(",");
    const values = [];
    let inQuote = false;
    let cur = "";
    for (let c = 0; c < line.length; c++) {
      const char = line[c];
      if (char === '"') {
        inQuote = !inQuote;
      } else if (char === ',' && !inQuote) {
        values.push(cur.trim().replace(/^"|"$/g, ''));
        cur = "";
      } else {
        cur += char;
      }
    }
    values.push(cur.trim().replace(/^"|"$/g, ''));

    const row = {};
    headers.forEach((h, idx) => {
      let val = values[idx] !== undefined ? values[idx] : "";
      if (["Age", "Purchase Frequency", "Engagement Score"].includes(h)) {
        val = parseInt(val, 10) || 0;
      } else if (["Average Order Value", "Total Spend", "Satisfaction Score"].includes(h)) {
        val = parseFloat(val) || 0.0;
      }
      row[h] = val;
    });
    rows.push(row);
  }
  return rows;
}

// Ingestion initialization
async function initData() {
  try {
    const res = await fetch("/data/raw/customer_segmentation_retention_sample.csv");
    if (!res.ok) throw new Error("HTTP error " + res.status);
    const csvText = await res.text();
    allCustomers = parseCSV(csvText);
    console.log(`Successfully loaded ${allCustomers.length} customer records.`);

    populateSlicers();
    applyFilters();
  } catch (err) {
    console.error("Failed to load CSV:", err);
    document.querySelector(".app-layout").innerHTML = `
      <div style="padding: 40px; text-align: center; color: #f87171;">
        <h2>Failed to load dataset</h2>
        <p style="color:#94a3b8; margin-top:8px;">Ensure server.py is running and customer_segmentation_retention_sample.csv is accessible.</p>
        <code style="color:#38bdf8; display:block; margin-top:12px;">Error: ${err.message}</code>
      </div>
    `;
  }
}

// Populate Slicer Dropdowns
function populateSlicers() {
  const segmentSelect = document.getElementById("slicer-segment");
  const citySelect = document.getElementById("slicer-city");

  const segments = [...new Set(allCustomers.map(c => c["Customer Segment"]))].sort();
  segments.forEach(seg => {
    const opt = document.createElement("option");
    opt.value = seg;
    opt.textContent = seg;
    segmentSelect.appendChild(opt);
  });

  const cities = [...new Set(allCustomers.map(c => c["City/Region"]))].sort();
  cities.forEach(city => {
    const opt = document.createElement("option");
    opt.value = city;
    opt.textContent = city;
    citySelect.appendChild(opt);
  });
}

// Apply Filters
function applyFilters() {
  const segVal = document.getElementById("slicer-segment").value;
  const retVal = document.getElementById("slicer-retention").value;
  const tierVal = document.getElementById("slicer-tier").value;
  const cityVal = document.getElementById("slicer-city").value;
  const searchVal = document.getElementById("search-input").value.trim().toLowerCase();

  filteredCustomers = allCustomers.filter(c => {
    if (segVal !== "ALL" && c["Customer Segment"] !== segVal) return false;
    
    // Synchronized retention status filter
    const effectiveRetention = retVal !== "ALL" ? retVal : (quickStatusFilter !== "ALL" ? quickStatusFilter : "ALL");
    if (effectiveRetention !== "ALL" && c["Retention Status"] !== effectiveRetention) return false;
    
    if (tierVal !== "ALL" && c["Loyalty Tier"] !== tierVal) return false;
    if (cityVal !== "ALL" && c["City/Region"] !== cityVal) return false;
    
    // Partial substring match for both Customer ID and Customer Name
    if (searchVal) {
      const custId = String(c["Customer ID"] || "").toLowerCase();
      const custName = String(c["Customer Name"] || "").toLowerCase();
      const idMatch = custId.includes(searchVal);
      const nameMatch = custName.includes(searchVal);
      if (!idMatch && !nameMatch) return false;
    }
    return true;
  });

  document.getElementById("cohort-count").textContent = filteredCustomers.length;

  updateKPIs();
  updateCharts();
  renderRiskMatrix();
  renderAuditTable();
}

function resetAllFilters() {
  document.getElementById("slicer-segment").value = "ALL";
  document.getElementById("slicer-retention").value = "ALL";
  document.getElementById("slicer-tier").value = "ALL";
  document.getElementById("slicer-city").value = "ALL";
  document.getElementById("search-input").value = "";
  quickStatusFilter = "ALL";
  updateQuickStatusPills();
  applyFilters();
}

function setQuickStatusFilter(status) {
  quickStatusFilter = status;
  document.getElementById("slicer-retention").value = status;
  updateQuickStatusPills();
  applyFilters();
}

function onRetentionDropdownChange() {
  const val = document.getElementById("slicer-retention").value;
  quickStatusFilter = val;
  updateQuickStatusPills();
  applyFilters();
}

function updateQuickStatusPills() {
  document.querySelectorAll(".pill-btn").forEach(btn => btn.classList.remove("active"));
  if (quickStatusFilter === "ALL") document.getElementById("btn-filter-all-table").classList.add("active");
  else if (quickStatusFilter === "Retained") document.getElementById("btn-filter-retained-table").classList.add("active");
  else if (quickStatusFilter === "At Risk") document.getElementById("btn-filter-atrisk-table").classList.add("active");
  else if (quickStatusFilter === "Churned") document.getElementById("btn-filter-churned-table").classList.add("active");
}

// Calculate DAX Measures
function updateKPIs() {
  const n = filteredCustomers.length;
  const totalRev = filteredCustomers.reduce((acc, c) => acc + c["Total Spend"], 0);
  const totalOrders = filteredCustomers.reduce((acc, c) => acc + c["Purchase Frequency"], 0);
  const aov = totalOrders > 0 ? totalRev / totalOrders : 0;
  const repeatCust = filteredCustomers.filter(c => c["Purchase Frequency"] > 1).length;
  const repeatRate = n > 0 ? repeatCust / n : 0;

  const retained = filteredCustomers.filter(c => c["Retention Status"] === "Retained").length;
  const atRisk = filteredCustomers.filter(c => c["Retention Status"] === "At Risk").length;
  const churned = filteredCustomers.filter(c => c["Retention Status"] === "Churned").length;

  const retentionShare = n > 0 ? retained / n : 0;
  const atRiskShare = n > 0 ? atRisk / n : 0;
  const churnShare = n > 0 ? churned / n : 0;

  const avgSpend = n > 0 ? totalRev / n : 0;
  const avgFreq = n > 0 ? totalOrders / n : 0;
  const avgEng = n > 0 ? filteredCustomers.reduce((acc, c) => acc + c["Engagement Score"], 0) / n : 0;
  const avgCSAT = n > 0 ? filteredCustomers.reduce((acc, c) => acc + c["Satisfaction Score"], 0) / n : 0;

  // Page 1 Elements
  document.getElementById("kpi-val-customers").textContent = n;
  document.getElementById("kpi-val-revenue").textContent = formatINR(totalRev, true);
  document.getElementById("kpi-val-revenue-raw").textContent = formatINR(totalRev);
  document.getElementById("kpi-val-aov").textContent = formatINR(aov);
  document.getElementById("kpi-val-orders").textContent = `${totalOrders} total orders`;
  document.getElementById("kpi-val-repeat-rate").textContent = formatPercent(repeatRate);
  document.getElementById("kpi-val-repeat-cust").textContent = `${repeatCust} / ${n} buyers (Freq > 1)`;
  
  // Retained and Churned with count and share
  document.getElementById("kpi-val-retained-count").textContent = retained;
  document.getElementById("kpi-val-retention-share").textContent = formatPercent(retentionShare);
  document.getElementById("kpi-val-churned-count").textContent = churned;
  document.getElementById("kpi-val-churn-share").textContent = formatPercent(churnShare);

  // Page 2 Elements
  document.getElementById("kpi-val-avg-spend").textContent = formatINR(avgSpend);
  document.getElementById("kpi-val-avg-freq").textContent = avgFreq.toFixed(2);
  document.getElementById("kpi-val-avg-eng").textContent = avgEng.toFixed(1) + " / 100";
  document.getElementById("kpi-val-avg-csat").textContent = avgCSAT.toFixed(1) + " / 5.0";

  // Page 3 Elements
  document.getElementById("kpi-val-p3-retained").textContent = retained;
  document.getElementById("kpi-val-p3-retained-share").textContent = formatPercent(retentionShare);
  document.getElementById("kpi-sub-p3-retained").textContent = `${retained} active portfolio accounts (0–60d)`;
  
  document.getElementById("kpi-val-p3-atrisk").textContent = atRisk;
  document.getElementById("kpi-val-p3-atrisk-share").textContent = formatPercent(atRiskShare);
  document.getElementById("kpi-sub-p3-atrisk").textContent = `${atRisk} lapsing accounts (61–150d)`;
  
  document.getElementById("kpi-val-p3-churned").textContent = churned;
  document.getElementById("kpi-val-p3-churned-share").textContent = formatPercent(churnShare);
  document.getElementById("kpi-sub-p3-churned").textContent = `${churned} inactive accounts (>150d)`;
  
  document.getElementById("kpi-val-p3-risk-share").textContent = formatPercent(atRiskShare);
}

// Chart Render / Update Dispatcher
function updateCharts() {
  if (typeof Chart === "undefined") return;

  renderP1SegmentsChart();
  renderP1RetentionChart();
  renderP1CategoryChart();
  renderP1ChannelChart();

  renderP2SegmentRevChart();
  renderP2RevShareChart();
  renderP2TierComboChart(); // The critical dual-axis combo chart!
  renderP2AOVSendChart();

  renderP3StatusAnalysisChart();
}

// Helper: Aggregate counts by key
function aggregateCounts(data, key) {
  const map = {};
  data.forEach(item => {
    const val = item[key] || "Unknown";
    map[val] = (map[val] || 0) + 1;
  });
  return map;
}

// Helper: Aggregate sums by key
function aggregateSums(data, key, sumKey) {
  const map = {};
  data.forEach(item => {
    const val = item[key] || "Unknown";
    map[val] = (map[val] || 0) + item[sumKey];
  });
  return map;
}

// Page 1 Chart 1: Customer Count by Segment
function renderP1SegmentsChart() {
  const ctx = document.getElementById("chart-p1-segments").getContext("2d");
  const counts = aggregateCounts(filteredCustomers, "Customer Segment");
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  const labels = sorted.map(s => s[0]);
  const data = sorted.map(s => s[1]);
  const total = data.reduce((a, b) => a + b, 0);

  if (charts.p1Segments) charts.p1Segments.destroy();
  charts.p1Segments = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Customers",
        data: data,
        backgroundColor: "rgba(40, 120, 181, 0.8)",
        borderColor: "#38bdf8",
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: { right: 15, left: 5 }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(ctx) {
              const val = ctx.raw;
              const pct = total > 0 ? ((val / total) * 100).toFixed(1) + "%" : "0.0%";
              return `Customers: ${val} (${pct} of portfolio)`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", precision: 0 }
        },
        y: {
          grid: { display: false },
          ticks: { color: "#e2e8f0", font: { size: 11.5, weight: "500" } }
        }
      }
    }
  });
}

// Page 1 Chart 2: Retention Status Donut
function renderP1RetentionChart() {
  const ctx = document.getElementById("chart-p1-retention").getContext("2d");
  const counts = aggregateCounts(filteredCustomers, "Retention Status");
  const labels = ["Retained", "At Risk", "Churned"];
  const data = labels.map(l => counts[l] || 0);
  const total = data.reduce((a, b) => a + b, 0);

  if (charts.p1Retention) charts.p1Retention.destroy();
  charts.p1Retention = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: [PALETTE.green, PALETTE.amber, PALETTE.red],
        borderWidth: 2,
        borderColor: "#111a2e"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: { top: 6, bottom: 6, left: 6, right: 6 }
      },
      plugins: {
        legend: {
          position: "right",
          labels: {
            color: "#e2e8f0",
            boxWidth: 12,
            font: { size: 12, weight: "600" },
            padding: 14,
            generateLabels: function(chart) {
              const d = chart.data;
              const bracketMap = {
                "Retained": "Retained (0–60d)",
                "At Risk": "At Risk (61–150d)",
                "Churned": "Churned (>150d)"
              };
              return d.labels.map((label, i) => {
                const val = d.datasets[0].data[i];
                const pct = total > 0 ? ((val / total) * 100).toFixed(1) + "%" : "0.0%";
                const displayLabel = bracketMap[label] || label;
                return {
                  text: `${displayLabel}: ${val} (${pct})`,
                  fillStyle: d.datasets[0].backgroundColor[i],
                  strokeStyle: d.datasets[0].borderColor,
                  lineWidth: 1,
                  hidden: false,
                  index: i
                };
              });
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(ctx) {
              const val = ctx.raw;
              const pct = total > 0 ? ((val / total) * 100).toFixed(1) + "%" : "0.0%";
              const bracketMap = {
                "Retained": "0–60 days",
                "At Risk": "61–150 days",
                "Churned": ">150 days"
              };
              const bracket = bracketMap[ctx.label] ? ` (${bracketMap[ctx.label]})` : "";
              return `${ctx.label}${bracket}: ${val} customers (${pct})`;
            }
          }
        }
      },
      cutout: "60%"
    }
  });
}

// Page 1 Chart 3: Revenue by Category
function renderP1CategoryChart() {
  const ctx = document.getElementById("chart-p1-categories").getContext("2d");
  const sums = aggregateSums(filteredCustomers, "Preferred Product Category", "Total Spend");
  const sorted = Object.entries(sums).sort((a, b) => b[1] - a[1]);
  const labels = sorted.map(s => s[0]);
  const data = sorted.map(s => s[1]);

  if (charts.p1Categories) charts.p1Categories.destroy();
  charts.p1Categories = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Revenue (INR)",
        data: data,
        backgroundColor: "rgba(56, 189, 248, 0.75)",
        borderColor: "#38bdf8",
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: { label: ctx => `Revenue: ${formatINR(ctx.raw)}` }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#94a3b8", maxRotation: 25 } },
        y: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", callback: v => formatINR(v, true) }
        }
      }
    }
  });
}

// Page 1 Chart 4: Revenue by Channel
function renderP1ChannelChart() {
  const ctx = document.getElementById("chart-p1-channels").getContext("2d");
  const sums = aggregateSums(filteredCustomers, "Purchase Channel", "Total Spend");
  const labels = Object.keys(sums);
  const data = Object.values(sums);

  if (charts.p1Channels) charts.p1Channels.destroy();
  charts.p1Channels = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: PALETTE.series.slice(0, labels.length),
        borderWidth: 2,
        borderColor: "#111a2e"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { color: "#e2e8f0", boxWidth: 12 } },
        tooltip: { callbacks: { label: ctx => `${ctx.label}: ${formatINR(ctx.raw)}` } }
      },
      cutout: "65%"
    }
  });
}

// Page 2 Chart 1: Revenue by Segment
function renderP2SegmentRevChart() {
  const ctx = document.getElementById("chart-p2-segment-rev").getContext("2d");
  const sums = aggregateSums(filteredCustomers, "Customer Segment", "Total Spend");
  const sorted = Object.entries(sums).sort((a, b) => b[1] - a[1]);
  const labels = sorted.map(s => s[0]);
  const data = sorted.map(s => s[1]);

  if (charts.p2SegmentRev) charts.p2SegmentRev.destroy();
  charts.p2SegmentRev = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Total Revenue",
        data: data,
        backgroundColor: "rgba(30, 58, 106, 0.8)",
        borderColor: "#60a5fa",
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => `Revenue: ${formatINR(ctx.raw)}` } }
      },
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", callback: v => formatINR(v, true) }
        },
        y: { grid: { display: false }, ticks: { color: "#e2e8f0" } }
      }
    }
  });
}

// Page 2 Chart 2: Segment Revenue Share %
function renderP2RevShareChart() {
  const ctx = document.getElementById("chart-p2-rev-share").getContext("2d");
  const sums = aggregateSums(filteredCustomers, "Customer Segment", "Total Spend");
  const totalRev = filteredCustomers.reduce((acc, c) => acc + c["Total Spend"], 0);
  const labels = Object.keys(sums);
  const data = labels.map(l => totalRev > 0 ? (sums[l] / totalRev) * 100 : 0);

  if (charts.p2RevShare) charts.p2RevShare.destroy();
  charts.p2RevShare = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: PALETTE.series.slice(0, labels.length),
        borderWidth: 2,
        borderColor: "#111a2e"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { color: "#e2e8f0", boxWidth: 12 } },
        tooltip: { callbacks: { label: ctx => `${ctx.label}: ${ctx.raw.toFixed(1)}%` } }
      },
      cutout: "60%"
    }
  });
}

// Page 2 Chart 3: Dual-Axis Combo Chart (Loyalty Tier: Revenue Bars + Customer Count Line)
function renderP2TierComboChart() {
  const ctx = document.getElementById("chart-p2-tier-combo").getContext("2d");
  const tiers = ["Platinum", "Gold", "Silver", "Bronze"];
  
  const revByTier = {};
  const custByTier = {};
  tiers.forEach(t => {
    revByTier[t] = 0;
    custByTier[t] = 0;
  });

  filteredCustomers.forEach(c => {
    const t = c["Loyalty Tier"];
    if (revByTier[t] !== undefined) {
      revByTier[t] += c["Total Spend"];
      custByTier[t] += 1;
    }
  });

  const revData = tiers.map(t => revByTier[t]);
  const custData = tiers.map(t => custByTier[t]);

  if (charts.p2TierCombo) charts.p2TierCombo.destroy();
  charts.p2TierCombo = new Chart(ctx, {
    type: "bar",
    data: {
      labels: tiers,
      datasets: [
        {
          type: "bar",
          label: "Total Revenue (INR)",
          data: revData,
          backgroundColor: "rgba(40, 120, 181, 0.75)",
          borderColor: "#38bdf8",
          borderWidth: 1,
          borderRadius: 4,
          yAxisID: "y"
        },
        {
          type: "line",
          label: "Customer Count",
          data: custData,
          borderColor: "#fbbf24",
          backgroundColor: "#fbbf24",
          borderWidth: 3,
          pointRadius: 5,
          pointHoverRadius: 7,
          tension: 0.25,
          yAxisID: "y1"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { position: "top", labels: { color: "#e2e8f0" } },
        tooltip: {
          callbacks: {
            label: function(ctx) {
              if (ctx.dataset.yAxisID === "y") {
                return `Revenue: ${formatINR(ctx.raw)}`;
              } else {
                return `Customers: ${ctx.raw} accounts`;
              }
            }
          }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#e2e8f0", font: { weight: "600" } } },
        y: {
          type: "linear",
          position: "left",
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#38bdf8", callback: v => formatINR(v, true) },
          title: { display: true, text: "Revenue (INR)", color: "#38bdf8" }
        },
        y1: {
          type: "linear",
          position: "right",
          grid: { drawOnChartArea: false },
          ticks: { color: "#fbbf24", precision: 0 },
          title: { display: true, text: "Customer Count", color: "#fbbf24" }
        }
      }
    }
  });
}

// Page 2 Chart 4: AOV vs Average Spend Comparison
function renderP2AOVSendChart() {
  const ctx = document.getElementById("chart-p2-aov-spend").getContext("2d");
  const segments = [...new Set(filteredCustomers.map(c => c["Customer Segment"]))].sort();

  const aovData = [];
  const spendData = [];

  segments.forEach(seg => {
    const custs = filteredCustomers.filter(c => c["Customer Segment"] === seg);
    const rev = custs.reduce((a, c) => a + c["Total Spend"], 0);
    const ord = custs.reduce((a, c) => a + c["Purchase Frequency"], 0);
    aovData.push(ord > 0 ? rev / ord : 0);
    spendData.push(custs.length > 0 ? rev / custs.length : 0);
  });

  if (charts.p2AovSpend) charts.p2AovSpend.destroy();
  charts.p2AovSpend = new Chart(ctx, {
    type: "bar",
    data: {
      labels: segments,
      datasets: [
        {
          label: "Average Order Value (AOV)",
          data: aovData,
          backgroundColor: "rgba(56, 189, 248, 0.7)",
          borderRadius: 4
        },
        {
          label: "Avg Customer Spend",
          data: spendData,
          backgroundColor: "rgba(30, 58, 106, 0.9)",
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top", labels: { color: "#e2e8f0" } },
        tooltip: { callbacks: { label: ctx => `${ctx.dataset.label}: ${formatINR(ctx.raw)}` } }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#94a3b8", maxRotation: 20 } },
        y: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", callback: v => formatINR(v, true) }
        }
      }
    }
  });
}

// Page 3 Chart: Revenue & Customer Count by Retention Status
function renderP3StatusAnalysisChart() {
  const ctx = document.getElementById("chart-p3-status-analysis").getContext("2d");
  const statuses = ["Retained", "At Risk", "Churned"];
  const revByStatus = aggregateSums(filteredCustomers, "Retention Status", "Total Spend");
  const custByStatus = aggregateCounts(filteredCustomers, "Retention Status");

  const revData = statuses.map(s => revByStatus[s] || 0);
  const custData = statuses.map(s => custByStatus[s] || 0);

  if (charts.p3Status) charts.p3Status.destroy();
  charts.p3Status = new Chart(ctx, {
    type: "bar",
    data: {
      labels: statuses,
      datasets: [
        {
          label: "Total Revenue (INR)",
          data: revData,
          backgroundColor: [PALETTE.green, PALETTE.amber, PALETTE.red],
          borderRadius: 4,
          yAxisID: "y"
        },
        {
          type: "line",
          label: "Customers",
          data: custData,
          borderColor: "#38bdf8",
          backgroundColor: "#38bdf8",
          borderWidth: 2,
          pointRadius: 5,
          yAxisID: "y1"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top", labels: { color: "#e2e8f0" } },
        tooltip: {
          callbacks: {
            label: function(ctx) {
              if (ctx.dataset.yAxisID === "y") return `Revenue: ${formatINR(ctx.raw)}`;
              return `Customers: ${ctx.raw}`;
            }
          }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#e2e8f0" } },
        y: {
          position: "left",
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", callback: v => formatINR(v, true) }
        },
        y1: {
          position: "right",
          grid: { drawOnChartArea: false },
          ticks: { color: "#38bdf8", precision: 0 }
        }
      }
    }
  });
}

// Page 3 Matrix Visual: At-Risk Distribution by Segment x Tier
function renderRiskMatrix() {
  const tbody = document.getElementById("risk-matrix-tbody");
  tbody.innerHTML = "";

  const segments = [
    "Champions",
    "Loyal Customers",
    "New / Potential Loyalist",
    "Needs Nurturing",
    "At Risk - High Value",
    "Hibernating"
  ];
  const tiers = ["Platinum", "Gold", "Silver", "Bronze"];

  const matrix = {};
  segments.forEach(s => {
    matrix[s] = { Platinum: 0, Gold: 0, Silver: 0, Bronze: 0, Total: 0 };
  });

  const tierTotals = { Platinum: 0, Gold: 0, Silver: 0, Bronze: 0, Total: 0 };

  filteredCustomers.filter(c => c["Retention Status"] === "At Risk").forEach(c => {
    const s = c["Customer Segment"];
    const t = c["Loyalty Tier"];
    if (matrix[s] && matrix[s][t] !== undefined) {
      matrix[s][t] += 1;
      matrix[s].Total += 1;
      tierTotals[t] += 1;
      tierTotals.Total += 1;
    }
  });

  segments.forEach(s => {
    const tr = document.createElement("tr");
    const isHighTierAtRisk = matrix[s].Platinum > 0 || matrix[s].Gold > 0;
    tr.innerHTML = `
      <td>${s}</td>
      <td class="${matrix[s].Platinum > 0 ? 'cell-high-risk' : ''}">${matrix[s].Platinum}</td>
      <td class="${matrix[s].Gold > 0 ? 'cell-high-risk' : ''}">${matrix[s].Gold}</td>
      <td>${matrix[s].Silver}</td>
      <td>${matrix[s].Bronze}</td>
      <td><strong>${matrix[s].Total}</strong></td>
    `;
    tbody.appendChild(tr);
  });

  // Total row
  const totTr = document.createElement("tr");
  totTr.className = "total-row";
  totTr.innerHTML = `
    <td>Total At-Risk</td>
    <td>${tierTotals.Platinum}</td>
    <td>${tierTotals.Gold}</td>
    <td>${tierTotals.Silver}</td>
    <td>${tierTotals.Bronze}</td>
    <td>${tierTotals.Total}</td>
  `;
  tbody.appendChild(totTr);
}

// Page 3 Customer-Level Risk Audit Table
function renderAuditTable() {
  const tbody = document.getElementById("customer-audit-tbody");
  tbody.innerHTML = "";

  // Sort customers
  const sorted = [...filteredCustomers].sort((a, b) => {
    let va = a[sortCol];
    let vb = b[sortCol];
    if (typeof va === "string") {
      return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
    }
    return sortAsc ? va - vb : vb - va;
  });

  sorted.forEach(c => {
    const tr = document.createElement("tr");

    let statusClass = "badge-status-retained";
    if (c["Retention Status"] === "At Risk") statusClass = "badge-status-atrisk";
    else if (c["Retention Status"] === "Churned") statusClass = "badge-status-churned";

    let tierClass = "badge-tier-silver";
    if (c["Loyalty Tier"] === "Platinum") tierClass = "badge-tier-platinum";
    else if (c["Loyalty Tier"] === "Gold") tierClass = "badge-tier-gold";
    else if (c["Loyalty Tier"] === "Bronze") tierClass = "badge-tier-bronze";

    tr.innerHTML = `
      <td><code>${c["Customer ID"]}</code></td>
      <td style="font-weight:600; color:#fff;">${c["Customer Name"]}</td>
      <td>${c["City/Region"]}</td>
      <td>${c["Last Purchase Date"]}</td>
      <td><span class="badge-status ${statusClass}">${c["Retention Status"]}</span></td>
      <td>${c["Customer Segment"]}</td>
      <td><span class="badge-tier ${tierClass}">${c["Loyalty Tier"]}</span></td>
      <td style="text-align:right;">${c["Purchase Frequency"]}</td>
      <td style="text-align:right; font-weight:700; color:#38bdf8;">${formatINR(c["Total Spend"])}</td>
      <td style="text-align:right;">${c["Engagement Score"]} / 100</td>
    `;
    tbody.appendChild(tr);
  });
}

// Table column sort handler
function sortTable(col) {
  if (sortCol === col) {
    sortAsc = !sortAsc;
  } else {
    sortCol = col;
    sortAsc = false;
  }
  renderAuditTable();
}

// Page switcher
function switchPage(pageId) {
  document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
  document.querySelectorAll(".report-page").forEach(page => page.classList.remove("active"));

  document.getElementById(`tab-${pageId}`).classList.add("active");
  document.getElementById(`page-${pageId}`).classList.add("active");

  // Trigger chart resize
  setTimeout(() => {
    Object.values(charts).forEach(c => {
      if (c && typeof c.resize === "function") c.resize();
    });
  }, 50);
}

// Run on page load
document.addEventListener("DOMContentLoaded", () => {
  initData();
});
