# AI Insurance Claim Prediction – Model Training Summary

This part of the project explores different regression approaches for predicting insurance settlement values using machine learning. The work is structured across multiple notebooks and organized into clearly separated model output folders.

## 1. `YaminReport.ipynb`

This notebook contains the **initial exploratory work** and **first round of model training**, including:

- **Data analysis** and inspection of missing values and categorical distributions.
- **Preprocessing** with basic imputation and encoding.
- **Model training**:
  - **Random Forest Regressor** (trained and evaluated independently).
  - **Stacking Regressor** using Random Forest, SVR, and Lasso as base models, with Ridge as the final estimator.

### Outputs:

- Results and trained files for the standalone **Random Forest** model are saved in:` Base_model/`
- Results and trained files for the **Stacking Regressor (initial version)** are saved in:
  `Stacking_model/`

---

## 2. `new.ipynb`

This notebook applies an **improved preprocessing pipeline**, addressing earlier limitations such as:

- Consistent handling of missing values.
- Better encoding and feature selection strategies.

The same models (Random Forest and Stacking Regressor) were re-trained using the updated dataset.

### Outputs:

- Results from models trained on the updated dataset are saved in:
  `New_Models/`

---

## Notes:

- Each output folder contains the trained model files, predictions, and key evaluation metrics (MAE, RMSE, R², MAPE).
