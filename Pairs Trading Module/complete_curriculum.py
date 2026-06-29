import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

cells = []

# Header
cells.append(nbf.v4.new_markdown_cell("""# Pairs Trading Module: Interactive Curriculum
Welcome to the Pairs Trading interactive notebook. In this module, you will explore the statistical foundations of pairs trading, implement pair selection, construct a spread, and generate trading signals.

*Instructions:* Throughout this notebook, you will see **[Markdown Prompts]**. You are expected to double-click the markdown cell and write your own explanation to demonstrate your understanding. You will also find coding exercises where the implementation is provided as a reference."""))

# Stationarity
cells.append(nbf.v4.new_markdown_cell("""## Stationarity & Unit Root Tests
Before we can trade a pair, we must ensure the relationship between the two assets is stable over time. We do this by testing for stationarity."""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: Stationarity
**[Markdown Prompt]**
Explain the concept of stationarity in time series analysis. Why is it important for pairs trading?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: The ADF Test
**[Markdown Prompt]**
What is the Augmented Dickey-Fuller (ADF) test? What is its null hypothesis?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: The KPSS Test
**[Markdown Prompt]**
What is the KPSS test? How does its null hypothesis differ from the ADF test? Why might we want to use both tests together?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Code: Stationarity Testing"""))

cells.append(nbf.v4.new_code_cell("""import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.tsa.stattools import adfuller, kpss
import matplotlib.pyplot as plt
import statsmodels.api as sm
from itertools import combinations

# Download stock data
data_aapl = yf.download('AAPL', start='2021-01-01', end='2024-01-01')['Close']
aapl_prices = data_aapl.dropna()

# Run adfuller(series) and print results
print("--- ADF Test ---")
adf_result = adfuller(aapl_prices)
print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"p-value: {adf_result[1]:.4f}")
print("Critical Values:")
for key, value in adf_result[4].items():
    print(f"\\t{key}: {value:.4f}")
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
    print(f"\\t{key}: {value:.4f}")
if kpss_result[1] < 0.05:
    print("Conclusion: Reject the null hypothesis. The series has a unit root (non-stationary).")
else:
    print("Conclusion: Fail to reject the null hypothesis. The series is stationary.")
"""))

# Pair Selection
cells.append(nbf.v4.new_markdown_cell("""## Pair Selection (Industry-Based)
Searching every possible combination of stocks leads to massive multiple-testing bias. Instead, we constrain our search to stocks within the same economic industry to ensure they share fundamental risk drivers."""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Code: Industry Pairing"""))

cells.append(nbf.v4.new_code_cell("""sectors = {
    'Tech': ['AAPL', 'MSFT', 'GOOGL', 'META'],
    'Financials': ['JPM', 'BAC', 'WFC', 'C'],
    'Energy': ['XOM', 'CVX', 'COP']
}

industry_pairs = []

# Iterate through the dictionary and use itertools.combinations to generate pairs within each sector
for industry, tickers in sectors.items():
    pairs = list(combinations(tickers, 2))
    industry_pairs.extend(pairs)

print(f"Total pairs generated: {len(industry_pairs)}")
print("Sample pairs:", industry_pairs[:5])
"""))

# Spread Construction
cells.append(nbf.v4.new_markdown_cell("""## Spread Construction & Hedge Ratio
Now that we have pairs, we need to construct a mean-reverting spread."""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: Log Prices
**[Markdown Prompt]**
Why do we typically use the log price difference instead of the raw nominal price difference when analyzing equity pairs over time?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Code: Log Prices and OLS Hedge Ratio"""))

cells.append(nbf.v4.new_code_cell("""# Download data for two related stocks
pair_data = yf.download(['AAPL', 'MSFT'], start='2021-01-01', end='2024-01-01')['Close']
pair_data = pair_data.dropna()

# Calculate log prices
log_aapl = np.log(pair_data['AAPL'])
log_msft = np.log(pair_data['MSFT'])

# Run an OLS regression to find hedge ratio
X = sm.add_constant(log_msft)
model = sm.OLS(log_aapl, X).fit()
hedge_ratio = model.params.iloc[1]

print(f"Hedge Ratio (Beta): {hedge_ratio:.4f}")

# Calculate the spread
spread = log_aapl - (hedge_ratio * log_msft)

plt.figure(figsize=(10,4))
spread.plot(title="AAPL vs MSFT Log Spread")
plt.axhline(spread.mean(), color='red', linestyle='--')
plt.show()
"""))

# Half-Life
cells.append(nbf.v4.new_markdown_cell("""## Mean Reversion & Half-Life
We have a spread, but how quickly does it mean-revert?"""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: Half-Life
**[Markdown Prompt]**
Explain what the 'half-life of mean reversion' represents in a trading context. How does an Ornstein-Uhlenbeck (OU) process relate to this metric?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Code: Calculating Half-Life"""))

cells.append(nbf.v4.new_code_cell("""# Calculate lagged spread and delta spread
spread_lag = spread.shift(1).dropna()
delta_spread = (spread - spread.shift(1)).dropna()

# Align data
spread_lag, delta_spread = spread_lag.align(delta_spread, join='inner')

# Run regression: delta_spread = lambda * spread_lag
model_hl = sm.OLS(delta_spread, spread_lag).fit()
lambda_val = model_hl.params.iloc[0]

# Calculate half-life
half_life = -np.log(2) / lambda_val
print(f"Speed of mean reversion (lambda): {lambda_val:.4f}")
print(f"Half-life: {half_life:.2f} days")
"""))

# Bollinger Bands
cells.append(nbf.v4.new_markdown_cell("""## Signal Generation with Bollinger Bands
We will use Bollinger Bands to generate dynamic entry and exit signals on our stationary spread."""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 My Explanation: Bollinger Bands
**[Markdown Prompt]**
Describe how Bollinger Bands are constructed. How can we use them to generate entry, exit, and stop-loss signals for our stationary pairs trading spread?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Code: Generating Signals"""))

cells.append(nbf.v4.new_code_cell("""# Define a lookback window (often tied to half-life, but we'll use 20 here)
window = 20

# Calculate rolling mean and rolling std dev of the spread
rolling_mean = spread.rolling(window=window).mean()
rolling_std = spread.rolling(window=window).std()

# Calculate upper band (mean + 2*std) and lower band (mean - 2*std)
upper_band = rolling_mean + (2 * rolling_std)
lower_band = rolling_mean - (2 * rolling_std)

# Generate a 'Position' signal based on crossover rules
signals = pd.Series(0, index=spread.index)
signals[spread < lower_band] = 1   # Long spread
signals[spread > upper_band] = -1  # Short spread

# Plot the spread, bands, and entry/exit signals
plt.figure(figsize=(12,6))
plt.plot(spread, label='Spread', color='blue', alpha=0.6)
plt.plot(rolling_mean, label='Rolling Mean', color='black', linestyle='--')
plt.plot(upper_band, label='Upper Band (+2 SD)', color='red', linestyle=':')
plt.plot(lower_band, label='Lower Band (-2 SD)', color='green', linestyle=':')

# Highlight signals
long_entries = spread[signals == 1]
short_entries = spread[signals == -1]
plt.scatter(long_entries.index, long_entries.values, color='green', marker='^', label='Long Entry')
plt.scatter(short_entries.index, short_entries.values, color='red', marker='v', label='Short Entry')

plt.title("Pairs Trading Signals: AAPL / MSFT")
plt.legend()
plt.show()
"""))

nb['cells'] = cells

output_path = r'c:\Users\ajdgh\Documents\GitHub\MAT-Education-\Pairs Trading Module\Pairs_Trading_Curriculum.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook completely filled out and sections removed at {output_path}")
