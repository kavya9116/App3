# 🇮🇳 Indian Union Budget Analyzer

An interactive **Streamlit** dashboard for analyzing and comparing the Union Budget of India across **20 major ministries** over **11 financial years** (FY 2013-14 to FY 2023-24).

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.x-3F4F75?logo=plotly&logoColor=white)

---

## ✨ Features

| Tab | Visualization | Description |
|-----|--------------|-------------|
| 📈 **Trend Analysis** | Line chart + Grouped bar chart | Track ministry budgets over time & year-on-year growth rates |
| 📊 **Year-on-Year Comparison** | Side-by-side bars + Waterfall | Compare any two financial years; see absolute budget changes |
| 🍩 **Share Breakdown** | Pie, Donut & Stacked Area charts | Understand each ministry's share of total budget |
| 🔥 **Heatmap** | Allocation + Growth Rate heatmaps | Spot high-spend areas and growth/decline patterns at a glance |
| 🏆 **Rankings** | Horizontal bar + Bump chart | Rank ministries by budget size; track rank changes over time |
| 📋 **Data Table** | Interactive table + CSV download | Browse raw data with totals; export for further analysis |

### Dashboard Controls (Sidebar)
- **Multi-select financial years** – choose which years to include
- **Multi-select ministries** – pick specific ministries for comparison
- **Color theme picker** – Viridis, Plasma, Inferno, Turbo, Sunset, Tealrose

### KPI Cards (Top)
- Total budget for the latest selected year (with % change)
- Top ministry by allocation
- Average ministry budget
- Years covered

---

## 🏛️ Ministries Covered

The dashboard includes data for **20 key Union Ministries/Departments**:

Defence · Home Affairs · Rural Development · Education · Health & Family Welfare · Agriculture & Farmers Welfare · Railways · Road Transport & Highways · Finance · Urban Development / Housing · Women & Child Development · Social Justice & Empowerment · Commerce & Industry · IT & Telecommunications · Science & Technology · Environment & Forests · Consumer Affairs & Food · Labour & Employment · Petroleum & Natural Gas · Textiles

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** installed on your system

### Installation

```bash
# 1. Navigate to the project directory
cd "Budget Year Wise"

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run main.py
```

The dashboard will open automatically in your default browser at **http://localhost:8501**.

---

## 📁 Project Structure

```
Budget Year Wise/
├── main.py              # Streamlit application (single file)
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── *.pdf                # Original Union Budget PDF documents (2013-2024)
```

---

## 📊 Data Source

Budget allocation figures (in **₹ Crores**) are sourced from the **Union Budget of India – Expenditure Budget** documents published by the Ministry of Finance, Government of India. Values represent **Budget Estimates** for each financial year.

The original PDF budget documents (FY 2013-14 to FY 2023-24) are included in this directory for reference.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend & Server | [Streamlit](https://streamlit.io/) |
| Visualizations | [Plotly](https://plotly.com/python/) |
| Data Processing | [Pandas](https://pandas.pydata.org/) + [NumPy](https://numpy.org/) |
| Language | Python 3.9+ |

---

## 📝 License

This project is for educational and analytical purposes. Budget data is publicly available from the Government of India.
