# Supply Chain Network Optimizer

A graph-based web application that models and optimizes real-world supply chain routes using the DataCo Smart Supply Chain dataset.

Built with **NetworkX**, **Streamlit**, and **Plotly**.

---

## Overview

This project answers two core supply chain questions:
- What is the correct order of operations in a supply chain?
- What is the cheapest or fastest route from a market to a destination city?

It uses two graph algorithms working together:
- **Kahn's Topological Sort** — structures the supply chain as a valid directed acyclic graph (DAG)
- **Dijkstra's Shortest Path** — finds the optimal route between any market and city

---

## Dataset

**DataCo Smart Supply Chain Dataset** — available on [Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

| Property | Value |
|----------|-------|
| Records | 180,519 orders |
| Features | 53 columns |
| Coverage | Global (5 markets, 154 countries, 3000+ cities) |
| Product types | Clothing, Sports Equipment, Electronics |

---

## Project Structure

```
project/
│
├── DataCoSupplyChainDataset.csv     # Raw dataset (download from Kaggle)
├── supply_chain_clean.csv           # Cleaned dataset (generated)
├── supply_chain_graph_v3.gml        # Final graph file (generated)
├── city_translations.json           # Spanish → English city name mapping (generated)
│
├── step1_load.py                    # Data loading and inspection
├── step2_clean.py                   # Data cleaning
├── step3.py                         # Graph construction with translations
├── step3_translate_cities.py        # Auto-translates city names via Google Translate
├── step4_algorithms_v2.py           # Algorithm testing
│
└── app.py                           # Streamlit web application
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/supply-chain-optimizer.git
cd supply-chain-optimizer
```

### 2. Install dependencies
```bash
pip install pandas numpy networkx streamlit matplotlib plotly deep-translator
```

### 3. Download the dataset
Download `DataCoSupplyChainDataset.csv` from [Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) and place it in the project root.

### 4. Run the pipeline

```bash
# Step 1: Load and inspect
python step1_load.py

# Step 2: Clean the data
python step2_clean.py

# Step 3: Translate city names (takes a few minutes)
python step3_translate_cities.py

# Step 4: Build the graph
python step3.py

# Step 5: Test algorithms
python step4_algorithms_v2.py

# Step 6: Launch the app
streamlit run app.py
```

---

## Application Features

### Tab 1 — Supply Chain Graph
- Interactive directed graph with 3,389 nodes and 3,442 edges
- Color-coded nodes: **Blue** = Markets, **Orange** = Regions, **Purple** = Countries, **Green** = Cities
- Filter graph by market to focus on a specific region
- Topological processing order displayed below the graph

### Tab 2 — Route Optimizer
- Select an origin **Market** and destination **City**
- City list automatically filters to only cities reachable from the selected market
- Optimize for **Cost** or **Speed**
- Displays step-by-step route with per-hop breakdown and total
- Highlights the optimal path in red on the graph

### Tab 3 — Dataset Explorer
- Average shipping cost by market
- Delivery status distribution (on-time vs late vs advance)
- Average delivery days by shipping mode
- Late delivery risk rate by market

---

## Algorithms

### Kahn's Topological Sort
Treats the supply chain as a DAG where goods flow strictly forward:
```
Market → Region → Country → City
```
Produces a valid processing order ensuring no stage is scheduled before its dependency.

### Dijkstra's Shortest Path
Finds the minimum-cost or fastest route between any market and city using real dataset values as edge weights:
- `avg_cost` — average order value along each route
- `avg_days` — average real shipping days along each route

---

## Graph Structure

| Level | Examples | Node Count |
|-------|----------|------------|
| Market | Africa, Europe, USCA | 5 |
| Region | Southeast Asia, Western Europe | 22 |
| Country | France, India, Brazil | 154 |
| City | Paris, Mumbai, São Paulo | 3,207 |

---

## Authors

- Dharmesh Sharma
- Mit Gandhi

---

## AI Usage

- **Google** — Dataset and topic search.
- **YouTube** — Implementation of Dijkstra and Kahn algorithms
- **Claude** — Translating the names, since most were in Spanish. The frontend of the project hosted using Streamlit.
- **ChatGPT** — Editing the ReadMe file.
