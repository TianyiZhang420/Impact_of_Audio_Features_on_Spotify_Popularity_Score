import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler

df = pd.read_csv("artifacts/spotify_data.csv")
df = df[df["popularity"] >= 5]  # Remove any extremely small values

# Create an empty dataset for cleaned data. Remove energy, valence, and acousticness with multicollinearity from previous correlation analysis
df_cleaned = pd.DataFrame()

# 1. Log transform of features
df_cleaned["duration_ms"] = np.log1p(df["duration_ms"])
df_cleaned["speechiness"] = np.log1p(df["speechiness"])
df_cleaned["acousticness"] = np.log1p(df["acousticness"])
df_cleaned["instrumentalness"] = np.log1p(df["instrumentalness"])

# 2. Standard scaling of features
standard_scaler = StandardScaler()
df_cleaned[["danceability", "liveness", "tempo", "loudness"]] = (
    standard_scaler.fit_transform(df[["danceability", "liveness", "tempo", "loudness"]])
)

# 3. Min Max scaling of features
min_max_scaler = MinMaxScaler()
df_cleaned[["key"]] = min_max_scaler.fit_transform(df[["key"]])

# 4. Add other features
df_cleaned["mode"] = df["mode"]
df_cleaned["popularity"] = df["popularity"]
df_cleaned["release_date"] = pd.to_datetime(df["release date"], errors="coerce")

# Extract the year from the 'release_date' and create a new 'release_year' column
df_cleaned["release_year"] = df_cleaned["release_date"].dt.year

df_cleaned["release_year"] = df_cleaned["release_year"].fillna(0).astype(int)

df_cleaned = df_cleaned.dropna()

df_cleaned = df_cleaned.reset_index(drop=True)

# Step 1: Select audio features and the release year
audio_features = [
    "danceability",
    "tempo",
    "liveness",
    "instrumentalness",
    "loudness",
    "speechiness",
    "key",
    "mode",
    "acousticness",
]
df_selected = df_cleaned[["release_year"] + audio_features]
df_selected = df_selected[df_selected["release_year"] > 1980]

df_selected.reset_index(drop=True, inplace=True)

# Step 2: Group the data by 'release_year' and calculate the mean of the audio features for each year
yearly_trends = df_selected.groupby("release_year")[audio_features].mean()

# Step 3: Plot the trends for each audio feature over time
plt.figure(figsize=(10, 6))

for feature in audio_features:
    plt.plot(yearly_trends.index, yearly_trends[feature], label=feature)

# Step 4: Customize the plot
plt.title("Trends in Audio Features Over Time")
plt.xlabel("Release Year")
plt.ylabel("Mean Value")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.savefig("images/time_based_analysis.png", bbox_inches="tight")
plt.show()
