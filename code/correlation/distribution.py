import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# read CSV
df = pd.read_csv("artifacts/spotify_data.csv")
print(len(df))
df["release date"] = pd.to_datetime(df["release date"])
df["year"] = df["release date"].dt.year

# choose variables to analyze, exclude the non-numeric variable）
variables = [
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
    "year",
]

# draw the charts
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 20))

for i, var in enumerate(variables, 1):
    plt.subplot(7, 2, i)  
    sns.histplot(df[var], kde=True, bins=30) 
    plt.title(f"Distribution of {var}", fontsize=12) 
    plt.xlabel(var)  
    plt.ylabel("Frequency")  

plt.tight_layout()

#save image
plt.savefig(
    "images/variable_distributions.png",
    bbox_inches="tight",
)

plt.show()
