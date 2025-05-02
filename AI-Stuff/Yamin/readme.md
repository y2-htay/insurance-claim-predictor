# AI Insurance Claim Prediction – Model Training Summary

This part of the project explores different regression approaches for predicting insurance settlement values using machine learning. The work is structured across multiple notebooks and organized into clearly separated model output folders.

---

## 1. `YaminReport.ipynb`

This notebook contains the **initial exploratory work** and **first round of model training**, including:

- **Data analysis** and inspection of missing values and categorical distributions.
- **Preprocessing** with basic imputation and encoding.
- **Model training**:
  - **Random Forest Regressor** (trained and evaluated independently).
  - **Stacking Regressor** using Random Forest, SVR, and Lasso as base models, with Ridge as the final estimator.

### Outputs (`Base_model/`):

- `random_forest_model.pkl` – saved Random Forest model
- `scaler.pkl` – StandardScaler used during training
- `predictions.csv` – actual vs predicted values
- `score_history.csv` – average of overall model metrics (MAE, RMSE, R², MAPE, Accuracy)
- `detailed_errors.csv` – per-row error details (absolute & percentage errors, R², RMSE)
- `feature_importance.csv` – ranked input features
- `model_parameters.json` – training parameters
- `scaler_details.json` – mean and scale info
- `training_results.json` – full metric output
- `prediction_plot.png` – visual scatterplot of actual vs predicted values

### Outputs (`Stacking_model/`):

- `stacking_model.pkl` – saved Stacking Regressor model
- `stacking_predictions.csv` – actual vs predicted values
- `detailed_errors.csv` – row-level errors (absolute/percentage), plus R² and RMSE
- `stacking_model_info.txt` – detailed breakdown of model structure and all hyperparameters used
- `prediction_plot.png` – scatterplot showing prediction accuracy

---

## 2. `new.ipynb`

This notebook applies an **improved preprocessing pipeline**, addressing earlier limitations such as:

- Consistent handling of missing values.
- Better encoding and feature selection strategies.

The same models (Random Forest and Stacking Regressor) were re-trained using the updated dataset.

### Outputs (`New_Models/`):

- `model_predictions.csv` – includes predictions from both models
- `detailed_errors.csv` – absolute & percentage errors, R², and RMSE for each model
- `prediction_plot.png` – actual vs predicted values plotted visually
- `stacking_model_info.txt` – detailed breakdown of model structure and all hyperparameters used
- `random_forest_model.pkl` – saved Random Forest model

---

## Evaluation Metrics

The following metrics are computed and saved:

- **MAE** – Mean Absolute Error
- **RMSE** – Root Mean Squared Error
- **R²** – Coefficient of Determination
- **MAPE** – Mean Absolute Percentage Error
- **Accuracy** – Defined as `100 - MAPE`

You can find:

- Summary scores in `score_history.csv`
- Detailed per-prediction metrics in `detailed_errors.csv`
- Visual graphs in `prediction_plot.png`


---

## Folder Overview

- `Base_model/`: Random Forest (original data)
- `Stacking_model/`: Stacking Regressor (original data)
- `New_Models/`: Random Forest & Stacking (retrained on improved data)

---
