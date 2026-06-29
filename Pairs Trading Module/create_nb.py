import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

cells = []

# Header
cells.append(nbf.v4.new_markdown_cell("""# Pairs Trading Module: Interactive Curriculum
Welcome to the Pairs Trading interactive notebook. In this module, you will explore the statistical foundations of pairs trading, implement pair selection, construct a spread, and generate trading signals.

*Instructions:* Throughout this notebook, you will see **[Markdown Prompts]**. You are expected to double-click the markdown cell and write your own explanation to demonstrate your understanding. You will also find coding exercises to implement the concepts."""))

# Section 1
cells.append(nbf.v4.new_markdown_cell("""## Section 1: Stationarity & Unit Root Tests
Before we can trade a pair, we must ensure the relationship between the two assets is stable over time. We do this by testing for stationarity."""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 Student Explanation: Stationarity
**[Markdown Prompt]**
Explain the concept of stationarity in time series analysis. Why is it important for pairs trading?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 Student Explanation: The ADF Test
**[Markdown Prompt]**
What is the Augmented Dickey-Fuller (ADF) test? What is its null hypothesis?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 Student Explanation: The KPSS Test
**[Markdown Prompt]**
What is the KPSS test? How does its null hypothesis differ from the ADF test? Why might we want to use both tests together?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Coding Exercise: Stationarity Testing
Import a price series (you can generate synthetic data or use `yfinance` to download a stock's history). Run both the ADF and KPSS tests using `statsmodels`. Print the p-values and interpret the results."""))

cells.append(nbf.v4.new_code_cell("""import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.tsa.stattools import adfuller, kpss

# TODO: Download stock data or generate a random walk
# TODO: Run adfuller(series) and print results
# TODO: Run kpss(series) and print results
"""))

# Section 2
cells.append(nbf.v4.new_markdown_cell("""## Section 2: Pair Selection (Industry-Based)
Searching every possible combination of stocks leads to massive multiple-testing bias. Instead, we constrain our search to stocks within the same economic industry to ensure they share fundamental risk drivers."""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Coding Exercise: Industry Pairing
Given a dictionary of stocks grouped by sector, write code to generate all unique pair combinations *only* within the same sector (e.g., Tech with Tech, Financials with Financials). Do not pair across sectors."""))

cells.append(nbf.v4.new_code_cell("""from itertools import combinations

sectors = {
    'Tech': ['AAPL', 'MSFT', 'GOOGL', 'META'],
    'Financials': ['JPM', 'BAC', 'WFC', 'C'],
    'Energy': ['XOM', 'CVX', 'COP']
}

industry_pairs = []

# TODO: Iterate through the dictionary and use itertools.combinations to generate pairs within each sector
# TODO: Print the total number of pairs generated
"""))

# Section 3
cells.append(nbf.v4.new_markdown_cell("""## Section 3: Spread Construction & Hedge Ratio
Now that we have pairs, we need to construct a mean-reverting spread."""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 Student Explanation: Log Prices
**[Markdown Prompt]**
Why do we typically use the log price difference instead of the raw nominal price difference when analyzing equity pairs over time?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Coding Exercise: Log Prices and OLS Hedge Ratio
Download data for a specific pair (e.g., AAPL and MSFT). Calculate the natural logarithm of their prices.
Then, use Ordinary Least Squares (OLS) regression to calculate the hedge ratio ($\beta$). 
Finally, construct the spread series: $Spread = \ln(Price_A) - \beta \ln(Price_B)$"""))

cells.append(nbf.v4.new_code_cell("""import statsmodels.api as sm
import matplotlib.pyplot as plt

# TODO: Download data for two related stocks
# TODO: Calculate log prices
# TODO: Run an OLS regression (remember to add a constant if necessary, though often omitted for pure hedge ratio)
# TODO: Extract the beta (hedge ratio)
# TODO: Calculate the spread and plot it
"""))

# Section 4
cells.append(nbf.v4.new_markdown_cell("""## Section 4: Mean Reversion & Half-Life
We have a spread, but how quickly does it mean-revert?"""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 Student Explanation: Half-Life
**[Markdown Prompt]**
Explain what the 'half-life of mean reversion' represents in a trading context. How does an Ornstein-Uhlenbeck (OU) process relate to this metric?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Coding Exercise: Calculating Half-Life
Write a function to calculate the half-life of the OLS spread you generated in Section 3."""))

cells.append(nbf.v4.new_code_cell("""# TODO: Run a regression of the change in the spread (\Delta Spread_t) against the lagged spread (Spread_{t-1})
# TODO: Extract the slope coefficient (\lambda)
# TODO: Calculate half-life using the formula: Half-life = -ln(2) / \lambda
# TODO: Print the half-life in days
"""))

# Section 5
cells.append(nbf.v4.new_markdown_cell("""## Section 5: Signal Generation with Bollinger Bands
We will use Bollinger Bands to generate dynamic entry and exit signals on our stationary spread."""))

cells.append(nbf.v4.new_markdown_cell("""### 📝 Student Explanation: Bollinger Bands
**[Markdown Prompt]**
Describe how Bollinger Bands are constructed. How can we use them to generate entry, exit, and stop-loss signals for our stationary pairs trading spread?

*Write your answer here...*"""))

cells.append(nbf.v4.new_markdown_cell("""### 💻 Coding Exercise: Generating Signals
Calculate the rolling mean and rolling standard deviation of the spread (using a window size related to your half-life). Construct upper and lower Bollinger Bands (e.g., +/- 2 standard deviations). Generate a signal array: 
* Go Long (+1) when the spread crosses below the lower band
* Go Short (-1) when it crosses above the upper band
* Exit (0) at the moving average"""))

cells.append(nbf.v4.new_code_cell("""# TODO: Define a lookback window (e.g., 20 days or based on half-life)
# TODO: Calculate rolling mean and rolling std dev of the spread
# TODO: Calculate upper band (mean + 2*std) and lower band (mean - 2*std)
# TODO: Generate a 'Position' column based on the crossover rules
# TODO: Plot the spread, the bands, and mark the entry/exit points visually
"""))

nb['cells'] = cells

output_path = r'c:\Users\ajdgh\Documents\GitHub\MAT-Education-\Pairs Trading Module\Pairs_Trading_Curriculum.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook created at {output_path}")
