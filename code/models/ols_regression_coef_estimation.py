import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


# Read cleaned data csv and create X features and y label
df = pd.read_csv("artifacts/cleaned_data.csv")
X = df.loc[:, df.columns != "popularity"]
y = df["popularity"]

# Fit a OLS regression for coef estimation and check p values for coefs
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

# plot the OLS regression summary
summary_str = results.summary().as_text()
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")
ax.text(0.01, 1, summary_str, fontsize=12, va="top", ha="left", family="monospace")
plt.savefig("images/ols_regression_summary.png", bbox_inches="tight", dpi=300)
