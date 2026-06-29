import nbformat as nbf
import os

def create_workbook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    # Header
    cells.append(nbf.v4.new_markdown_cell("# Pairs Trading: Exercise Workbook\n\n**Instructions:** The theory and explanations are provided below. Your task is to fill in the missing code `___` to get the cells working."))
    
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

# Download data for the last 3 years
print("Downloading data...")
data = yf.download(tickers, start="2021-01-01", end="2024-01-01")['Close']
data = data.dropna()
print("Data downloaded.")
"""))

    # Section 1
    cells.append(nbf.v4.new_markdown_cell("## Stationarity & Unit Root Tests\nBefore we can trade a pair, we must ensure the relationship between the two assets is stable over time."))
    cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: The ADF Test
The **Augmented Dickey-Fuller (ADF) test** checks whether a time series has a unit root, which would mean it is non-stationary.
*   **Null Hypothesis (H0):** The series has a unit root (it is NON-STATIONARY).
*   **Alternative Hypothesis (H1):** The series is stationary.
If the p-value is < 0.05, we reject the null hypothesis and assume the series is stationary."""))
    cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: The KPSS Test
The **KPSS test** is another unit root test, but its hypotheses are flipped compared to the ADF test.
*   **Null Hypothesis (H0):** The series is STATIONARY around a deterministic trend.
*   **Alternative Hypothesis (H1):** The series has a unit root (non-stationary).
If the p-value is < 0.05, we reject the null hypothesis, meaning the series is non-stationary. Using both tests provides a robust check for stationarity."""))
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
    # Generate pairs for this group
    pairs = list(combinations(___, ___))
    industry_pairs.extend(pairs)

print(f"Total intra-industry pairs generated: {len(industry_pairs)}")
print(industry_pairs[:5])
"""))

    # Section 3
    cells.append(nbf.v4.new_markdown_cell("## Spread Construction & Hedge Ratio"))
    cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: Log Prices
We use **log prices** because changes in logarithmic prices approximate percentage returns. By modeling the spread of log prices ($Spread = \ln(A) - \beta \ln(B)$), the spread represents the relative percentage difference between the two assets, making the strategy invariant to the absolute nominal price levels of the stocks. It also helps stabilize the variance over time."""))
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
    cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: Half-Life
The **half-life of mean reversion** tells us the average time it takes for a spread to revert halfway back to its historical mean after deviating from it. 
It is derived by fitting an **Ornstein-Uhlenbeck (OU) process** to the spread, regressing the change in the spread ($\Delta y_t$) against its lagged value ($y_{t-1}$). The slope coefficient ($\lambda$) represents the speed of mean reversion. We calculate the half-life as `-ln(2) / lambda`."""))
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
    cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: Bollinger Bands
**Bollinger Bands** consist of a rolling simple moving average (SMA) and two outer bands representing $+/- Z$ standard deviations away from the SMA. 
*   **Entry Signals:** If the spread is stationary, we expect it to revert to the mean. Therefore, we **Go Long** when the spread drops below the lower band (it is undervalued), and we **Go Short** when it spikes above the upper band (it is overvalued).
*   **Exit Signal:** We exit the position when the spread crosses the moving average (mean)."""))
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

    nb['cells'] = cells
    return nb

output_dir = r'c:\\Users\\ajdgh\\Documents\\GitHub\\MAT-Education-\\Pairs Trading Module'
wb = create_workbook()
with open(os.path.join(output_dir, 'Pairs_Trading_Workbook.ipynb'), 'w', encoding='utf-8') as f:
    nbf.write(wb, f)

print("Workbook updated successfully.")
