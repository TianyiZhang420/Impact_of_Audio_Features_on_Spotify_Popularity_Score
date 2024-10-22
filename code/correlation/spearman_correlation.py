import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np


# read CSV
df = pd.read_csv("artifacts/spotify_data.csv")
# If we want to use the 'year' variable, we can use the following lines
#df['release date'] = pd.to_datetime(df['release date'])
#df['year'] = df['release date'].dt.year

variables = [
    "popularity",
    "duration (ms)",
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]

# Spearman
spearman_corr = df[variables].corr(method="spearman")

print(spearman_corr)


plt.figure(figsize=(12, 10))

sns.heatmap(
    spearman_corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    annot_kws={"size": 10},
    xticklabels=variables,
    yticklabels=variables,
    cbar_kws={"shrink": 0.8},
)


plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)


plt.title("Spearman Correlation Matrix of Music Features")


plt.savefig(
    "images/spearman_correlation.png",
    bbox_inches="tight",
)


plt.show()

variables_vif = [
    "duration (ms)",
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]

df_cleaned_vif = df[variables_vif]

df_cleaned_vif = df_cleaned_vif.replace([np.inf, -np.inf], np.nan).dropna()

vif_data = pd.DataFrame()
vif_data["Feature"] = df_cleaned_vif.columns
vif_data["VIF"] = [
    variance_inflation_factor(df_cleaned_vif.values, i)
    for i in range(df_cleaned_vif.shape[1])
]

print(vif_data)
