import nbformat as nbf
import os

nb_path = r'c:\Users\ajdgh\Documents\GitHub\MAT-Education-\Pairs Trading Module\Pairs_Trading_Curriculum.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'markdown':
        # Replace "Student Explanation" with "My Explanation"
        if "Student Explanation" in cell.source:
            cell.source = cell.source.replace("Student Explanation", "My Explanation")
            
    if cell.cell_type == 'code':
        # Fill in the ADF test section
        if "TODO: Run adfuller(series) and print results" in cell.source:
            cell.source = """import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.tsa.stattools import adfuller, kpss

# Download stock data
data = yf.download('AAPL', start='2021-01-01', end='2024-01-01')['Close']
data = data.dropna()
aapl_prices = data

# Run adfuller(series) and print results
print("--- ADF Test ---")
adf_result = adfuller(aapl_prices)
print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"p-value: {adf_result[1]:.4f}")
print("Critical Values:")
for key, value in adf_result[4].items():
    print(f"\t{key}: {value:.4f}")
if adf_result[1] < 0.05:
    print("Conclusion: Reject the null hypothesis. The series is stationary.")
else:
    print("Conclusion: Fail to reject the null hypothesis. The series has a unit root (non-stationary).")

# Run kpss(series) and print results
print("\\n--- KPSS Test ---")
import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    kpss_result = kpss(aapl_prices)
print(f"KPSS Statistic: {kpss_result[0]:.4f}")
print(f"p-value: {kpss_result[1]:.4f}")
print("Critical Values:")
for key, value in kpss_result[3].items():
    print(f"\t{key}: {value:.4f}")
if kpss_result[1] < 0.05:
    print("Conclusion: Reject the null hypothesis. The series has a unit root (non-stationary).")
else:
    print("Conclusion: Fail to reject the null hypothesis. The series is stationary.")
"""

with open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook updated successfully.")
