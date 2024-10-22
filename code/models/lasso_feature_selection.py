import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso, LassoCV
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


# Read cleaned data csv and create X features and y label
df = pd.read_csv("artifacts/cleaned_data.csv")
X = df.loc[:, df.columns != "popularity"]
y = df["popularity"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Fit a lasso regression with 5 fold cross validation
lasso_cv = LassoCV(alphas=[0.2, 0.4, 0.6, 0.8], cv=5)
lasso_cv.fit(X_train, y_train)

# Obtain optimal alpha
optimal_alpha = lasso_cv.alpha_

# Fit a lasso regression on trainning data with optimal alpha value
lasso = Lasso(alpha=optimal_alpha)
lasso.fit(X_train, y_train)
coef = lasso.coef_
features = X.columns
feature_importance = pd.DataFrame(
    {"Feature": features, "Coefficient": coef}
).sort_values(by="Coefficient", ascending=True)

# Plot feature coefficients
plt.figure(figsize=(10, 5))
plt.barh(feature_importance["Feature"], feature_importance["Coefficient"])
plt.xlabel("Coefficient")
plt.ylabel("Feature")
plt.title("Lasso Feature Selection")
plt.savefig("images/lasso_feature_selection.png", bbox_inches="tight")
plt.show()

# Get mse on testing data
y_pred = lasso.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error (MSE): {mse:.4f}")
