import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("artifacts/cleaned_data.csv")

# Step 1: Calculate the 90th percentile of the popularity score
top_10_percent_threshold = df["popularity"].quantile(0.90)

# Step 2: Create a new column indicating if the song is in the Top 10% or not
df["top_10_percent"] = df["popularity"] >= top_10_percent_threshold

# Step 3: Select the audio features to compare
audio_features = [
    "danceability",
    "tempo",
    "liveness",
    "instrumentalness",
    "loudness",
    "speechiness",
]

# Step 4: Group the data by 'top_10_percent' and calculate the mean of the audio features for each group
feature_means = df.groupby("top_10_percent")[audio_features].mean()

# Step 5: Display the comparison
print("Average Audio Features - Top 10% vs. Other Songs:")
print(feature_means)

feature_means.T.plot(kind="bar", figsize=(10, 6))
plt.title("Average Audio Features Comparison (Top 10% vs. Others)")
plt.xlabel("Audio Features")
plt.ylabel("Mean Value")
plt.xticks(rotation=45)
plt.savefig("images/avg_audio_features_comparison_top_10per.png", bbox_inches="tight")
plt.show()
