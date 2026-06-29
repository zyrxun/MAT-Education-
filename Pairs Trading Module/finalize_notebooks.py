import nbformat as nbf
import os
import shutil

dir_path = r'c:\Users\ajdgh\Documents\GitHub\MAT-Education-\Pairs Trading Module'

# 1. Rename Solutions to Textbook and update its header
solutions_path = os.path.join(dir_path, 'Pairs_Trading_Solutions.ipynb')
textbook_path = os.path.join(dir_path, 'Pairs_Trading_Textbook.ipynb')

if os.path.exists(solutions_path):
    with open(solutions_path, 'r', encoding='utf-8') as f:
        tb = nbf.read(f, as_version=4)
    # Update first cell
    if tb.cells and tb.cells[0].cell_type == 'markdown':
        tb.cells[0].source = "# Pairs Trading: Textbook & Reference\n\n**Instructions:** Read through this notebook and take notes. It contains the complete theory and fully functional code for the pairs trading pipeline."
    with open(textbook_path, 'w', encoding='utf-8') as f:
        nbf.write(tb, f)
    os.remove(solutions_path)

# 2. Delete the old Curriculum notebook to keep it to strictly TWO notebooks
curriculum_path = os.path.join(dir_path, 'Pairs_Trading_Curriculum.ipynb')
if os.path.exists(curriculum_path):
    os.remove(curriculum_path)

# 3. Rewrite the Workbook so both text AND code are blank
wb = nbf.v4.new_notebook()
cells = []

# Header
cells.append(nbf.v4.new_markdown_cell("# Pairs Trading: Exercise Workbook\n\n**Instructions:** Fill in the markdown prompts using your notes. Fill in the missing code `___` to complete the programming exercises."))

# Section 0: Data
cells.append(nbf.v4.new_markdown_cell("## Data Download\nFirst, we download a sample universe of 10 stocks across different industries."))
cells.append(nbf.v4.new_code_cell("""import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
from itertools import combinations

# 10 Stock Universe grouped by Industry
industry_map = {
    'Tech': ['AAPL', 'MSFT', 'GOOGL', 'META'],
    'Financials': ['JPM', 'BAC', 'WFC'],
    'Energy': ['XOM', 'CVX', 'COP']
}
tickers = [ticker for group in industry_map.values() for ticker in group]

print("Downloading data...")
data = yf.download(tickers, start="2021-01-01", end="2024-01-01")['Close']
data = data.dropna()
print("Data downloaded.")
"""))

# Section 1
cells.append(nbf.v4.new_markdown_cell("## Stationarity & Unit Root Tests\nBefore we can trade a pair, we must ensure the relationship between the two assets is stable over time."))
cells.append(nbf.v4.new_markdown_cell("""### 📝 Explanation: The ADF Test
*Explain what the Augmented Dickey-Fuller test is and state its null hypothesis here.*"""))
cells.append(nbf.v4.new_markdown_cell("""### 📝 Explanation: The KPSS Test
*Explain what the KPSS test is and how its null hypothesis differs from the ADF test here.*"""))
cells.append(nbf.v4.new_markdown_cell("### 💻 Code: Stationarity Testing"))
cells.append(nbf.v4.new_code_cell("""# Extract AAPL prices
aapl_prices = data['AAPL']

# TODO: Run the ADF test on AAPL prices
adf_result = ___(aapl_prices)
print("ADF p-value:", adf_result[1])

# TODO: Run the KPSS test on AAPL prices
import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    kpss_result = ___(aapl_prices)
print("KPSS p-value:", kpss_result[1])
"""))

# Section 2
cells.append(nbf.v4.new_markdown_cell("## Pair Selection (Industry-Based)\nGenerate all unique pairs within the same industry to ensure they share fundamental risk drivers."))
cells.append(nbf.v4.new_code_cell("""industry_pairs = []

# TODO: Iterate through `industry_map` and use combinations to create pairs
for industry, group_tickers in industry_map.items():
    pairs = list(combinations(___, ___))
    industry_pairs.extend(pairs)

print(f"Total intra-industry pairs generated: {len(industry_pairs)}")
print(industry_pairs[:5])
"""))

# Section 3
cells.append(nbf.v4.new_markdown_cell("## Spread Construction & Hedge Ratio"))
cells.append(nbf.v4.new_markdown_cell("""### 📝 Explanation: Log Prices
*Why do we use log prices instead of raw prices for spread construction? Explain here.*"""))
cells.append(nbf.v4.new_markdown_cell("### 💻 Code: Spread Construction (OLS)\nLet's test the pair AAPL and MSFT."))
cells.append(nbf.v4.new_code_cell("""# TODO: Calculate log prices for AAPL and MSFT
log_aapl = np.log(___)
log_msft = np.log(___)

# TODO: Calculate Hedge Ratio using OLS (Y = AAPL, X = MSFT)
# Remember to add a constant to X using sm.add_constant()
X = sm.add_constant(___)
model = sm.OLS(___, X).fit()
hedge_ratio = model.params.iloc[1]

print(f"Hedge Ratio: {hedge_ratio}")

# TODO: Calculate the spread
spread = ___ - (hedge_ratio * ___)
spread.plot(title="AAPL - MSFT Log Spread")
plt.show()
"""))

# Section 4
cells.append(nbf.v4.new_markdown_cell("## Mean Reversion & Half-Life"))
cells.append(nbf.v4.new_markdown_cell("""### 📝 Explanation: Half-Life
*Explain what the half-life of mean reversion is and how it is calculated using an Ornstein-Uhlenbeck process.*"""))
cells.append(nbf.v4.new_code_cell("""# TODO: Calculate lagged spread and delta spread
spread_lag = spread.___()
spread_lag = spread_lag.dropna()
delta_spread = spread - ___
delta_spread = delta_spread.dropna()

# Ensure alignment
spread_lag, delta_spread = spread_lag.align(delta_spread, join='inner')

# TODO: Run OLS to find lambda (slope)
X_hl = spread_lag
model_hl = sm.OLS(delta_spread, X_hl).fit()
lambda_val = model_hl.params.iloc[0]

# TODO: Calculate half-life
half_life = -np.log(2) / ___
print(f"Half-life: {half_life} days")
"""))

# Section 5
cells.append(nbf.v4.new_markdown_cell("## Signal Generation with Bollinger Bands"))
cells.append(nbf.v4.new_markdown_cell("""### 📝 Explanation: Bollinger Bands
*Explain how Bollinger Bands are constructed and the logic for generating Long/Short signals for a mean-reverting spread.*"""))
cells.append(nbf.v4.new_code_cell("""# TODO: Define lookback window (e.g., 20 days)
window = ___

# TODO: Calculate rolling mean and standard deviation
rolling_mean = spread.rolling(window=window).___()
rolling_std = spread.rolling(window=window).___()

# TODO: Construct Upper and Lower Bands (2 standard deviations)
upper_band = rolling_mean + (___ * rolling_std)
lower_band = rolling_mean - (___ * rolling_std)

# TODO: Generate Signals
# 1 if spread < lower_band, -1 if spread > upper_band, 0 otherwise
signals = pd.Series(0, index=spread.index)
signals[spread < ___] = 1
signals[spread > ___] = -1

# Plot
plt.figure(figsize=(10,6))
plt.plot(spread, label='Spread')
plt.plot(rolling_mean, label='Moving Average', color='black', linestyle='--')
plt.plot(upper_band, label='Upper Band', color='red', linestyle=':')
plt.plot(lower_band, label='Lower Band', color='green', linestyle=':')
plt.legend()
plt.title("Bollinger Bands for AAPL/MSFT Spread")
plt.show()
"""))

wb['cells'] = cells

workbook_path = os.path.join(dir_path, 'Pairs_Trading_Workbook.ipynb')
with open(workbook_path, 'w', encoding='utf-8') as f:
    nbf.write(wb, f)

print("Finalization complete. Only Textbook and Workbook remain.")
