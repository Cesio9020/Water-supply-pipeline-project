# 🚰 Water Supply System Design & Economic Analysis

This project models and evaluates a water supply system over a 40-year horizon using Python.

It combines **hydraulic analysis, demand forecasting, and economic evaluation** into a structured and testable pipeline to support engineering decision-making.

---

## 📌 Overview

The goal of this project is to compare alternative pipe diameters based on **total lifecycle cost**, considering:

- Water demand evolution
- Pump operation
- Energy consumption
- Discounted future costs

All costs are evaluated relative to the **base year 2003**.

---

## ⚙️ Features

- 📈 Population forecasting using:
  - Arithmetic method
  - Linear regression

- 💧 Water demand estimation for:
  - Population
  - Hotel consumption
  - Industrial consumption

- 🔢 Flow calculations:
  - Average daily flow (Qmd)
  - Peak daily flow (Qpd)
  - Peak instantaneous flow (Qpi)

- ⚙️ Pump operation modeling:
  - Daily operating time

- ⚡ Energy cost estimation:
  - Different pipe diameters (250 mm and 315 mm)

- 💰 Economic analysis:
  - Discounted cash flow (present value)

- ✅ Automated testing using **pytest**

---

## 🧠 Methodology

The pipeline follows these steps:

1. Fit a population growth model from census data  
2. Forecast population over 40 years  
3. Estimate hotel and industrial water demand  
4. Compute total demand including network losses  
5. Calculate pump operating time  
6. Estimate annual energy costs  
7. Discount future costs to present value  
8. Compare alternatives based on total cost  

---

## 🏗️ Project Structure

```text
Hydraulic-System/
│
├── config.py
├── population.py
├── demand.py
├── hydraulics.py
├── economics.py
├── pipeline.py
├── main.py
│
├── tests/
│   └── test_pipeline.py
│
├── images/
│
├── requirements.txt
└── README.md