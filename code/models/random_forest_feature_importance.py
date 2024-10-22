import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV


# Read cleaned data csv and create X features and y label
df = pd.read_csv("artifacts/cleaned_data.csv")
X = df.loc[:, df.columns != "popularity"]
y = df["popularity"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Grid search cross validation on trainning data for the best parameters
rf = RandomForestRegressor(random_state=42)
param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [5, 10, 15],
    "min_samples_split": [2, 3, 4],
    "min_samples_leaf": [1, 2, 3],
}
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    scoring="neg_mean_squared_error",
    cv=5,
    n_jobs=-1,
    verbose=1,
)
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_

# Fit random forest with the best parameters to get feature importance
best_rf = RandomForestRegressor(**best_params, random_state=42)
best_rf.fit(X_train, y_train)
importances = best_rf.feature_importances_

# Create a DataFrame to plot and visualize the feature importance
feature_importance = pd.DataFrame(
    {"Feature": X.columns, "Importance": importances}
).sort_values(by="Importance", ascending=True)
plt.figure(figsize=(10, 6))
plt.barh(feature_importance["Feature"], feature_importance["Importance"])
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Random Forest Feature Importance")
plt.savefig("images/random_forest_feature_importance.png", bbox_inches="tight")
plt.show()

# Get MSE on testing data
y_pred = best_rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
