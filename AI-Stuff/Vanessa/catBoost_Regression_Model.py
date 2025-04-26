import pandas as pd
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "processed.csv"
df = pd.read_csv(file_path)

# Display basic info
print("First few rows:")
print(df.head())

print("\nColumn names:")
print(df.columns)

print("\nMissing values:")
print(df.isnull().sum())

# Separate features and target variable
X = df.drop(columns=['SettlementValue'])
y = df['SettlementValue']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nTraining data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)

# Train a CatBoostRegressor model
model = CatBoostRegressor(
    iterations=300,
    depth=4,
    learning_rate=0.05,
    loss_function='RMSE',
    verbose=100
)

model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=50)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = mse**0.5
print("\nRMSE:", rmse)

# Summary stats for SettlementValue
print("Average SettlementValue:", df['SettlementValue'].mean())
print("Minimum SettlementValue:", df['SettlementValue'].min())
print("Maximum SettlementValue:", df['SettlementValue'].max())
print("Standard Deviation of SettlementValue:", df['SettlementValue'].std())

# Plot Feature Importances
feature_importances = model.get_feature_importance()
feature_names = X.columns

plt.figure(figsize=(12, 8))
plt.barh(feature_names, feature_importances)
plt.xlabel("Feature Importance")
plt.title("CatBoost Feature Importances")
plt.tight_layout()
plt.show()

# Plot Residuals
residuals = y_test - y_pred

plt.figure(figsize=(10, 6))
sns.histplot(residuals, bins=30, kde=True)
plt.title("Residual Distribution")
plt.xlabel("Residual (True - Predicted)")
plt.tight_layout()
plt.show()

# OPTIONAL: Grid Search for Hyperparameter Tuning
"""
from sklearn.model_selection import GridSearchCV

params = {
    'depth': [4, 6, 8],
    'learning_rate': [0.05, 0.1, 0.2],
    'iterations': [100, 300, 500]
}

grid = GridSearchCV(
    CatBoostRegressor(loss_function='RMSE', verbose=0),
    param_grid=params,
    cv=3
)

grid.fit(X_train, y_train)

print("Best parameters:", grid.best_params_)
print("Best RMSE score from CV:", grid.best_score_)
"""

# ...........................

'''
GRIDSEARCH RESULTS:
Best parameters: {'depth': 4, 'iterations': 300, 'learning_rate': 0.05}
Best RMSE score from CV: 0.34312325786485137
'''











# ................. EVALUATION STUFF ...........................

'''
EVALUATION OF GRIDSEARCH RESULTS:
depth=4: Shallower trees performed better than deeper ones (6, 8)

iterations=300: Not the highest tested (500), suggesting 300 was a sweet spot for convergence

learning_rate=0.05: A smaller learning rate, often more stable and generalizes better
'''

# ...........................

'''
EVALUATION OF MODEL:

OVERFITTING:
The model stopped early to prevent overfitting — good behavior.

FEATURE IMPORTANCE:
Injury_Prognosis feature importance:
If Injury_Prognosis has the highest feature importance, it means most of the model’s predictive power is coming from this one feature.
That’s not necessarily bad — but here’s what it could mean:

Possibilities:
Injury_Prognosis is strongly correlated with SettlementValue (which makes sense — more serious injury, higher compensation).
Other features might be redundant or weakly predictive.
Data leakage? Could Injury_Prognosis be derived from or closely related to SettlementValue?

Correlation Check:
'''
# print(df[['SettlementValue', 'Injury_Prognosis']].corr())
'''
RESULTS:
SettlementValue          1.000000          0.538524 
Injury_Prognosis         0.538524          1.000000

The correlation between Injury_Prognosis and SettlementValue is ~0.54.
That’s a moderate-to-strong positive correlation, which confirms that the two move together — as injury severity goes up, the settlement amount tends to increase too.
This makes logical sense for an insurance model — more severe injuries lead to higher claim settlements.

RESIDUAL DISTRIBUTION GRAPH:
The highest count (~80) being at -0.3 means The model is often predicting ~0.3 units higher than the actual SettlementValue.
This is a mild overprediction bias.

Mean of Residuals Check (should be close to 0 if there's no bias):
'''
# print("Mean residual:", residuals.mean())
'''
RESULT:
Mean residual: -0.023819176030336144

The mean residual of -0.0238 is very close to zero, which indicates that the model’s overall bias is quite small.
This is a good sign because it shows the model isn't significantly overestimating or underestimating the SettlementValue on average.
The slightly negative mean residual suggests there might be a small systematic overprediction.
However, the magnitude is so small (just ~0.02) that it likely won't have a major impact on your predictions.
'''