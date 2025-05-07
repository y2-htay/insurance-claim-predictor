# CatBoost Regression on Synthetic Claims Dataset

This notebook demonstrates how to perform a complete end-to-end regression analysis using the `CatBoostRegressor` on a synthetic insurance claims dataset. The model predicts the **SettlementValue** for each claim based on a variety of features such as claim timing, accident details, and other contextual factors.

## Dataset

**File Used:** `Synthetic_Data_For_Students.csv`

Contains claim records with:

- Dates of accidents and claims  
- Categorical descriptors (e.g., region, type)  
- Numerical attributes  
- **Target variable:** `SettlementValue`

## Workflow Summary

1. **Setup & Libraries**  
   Installs and imports required packages such as:  
   `catboost`, `pandas`, `numpy`, `scikit-learn`, `seaborn`, `matplotlib`, `scipy`

2. **Data Cleaning**  
   - Handles missing values:  
     - Fills numeric features with **median**  
     - Fills categorical features with **mode**
   - Checks for and handles skewness in `SettlementValue` using **log transformation** if highly skewed  
   - Processes datetime columns to extract `Days_To_Claim`

3. **Feature Engineering**  
   - Drops original date columns after feature extraction  
   - Uses **CatBoost’s internal categorical encoding** — no need for manual label encoding

4. **Train/Test Split**  
   - Splits the dataset into training and testing sets using `train_test_split`

5. **Cross-Validation**  
   - Applies `cross_validate` with 5-fold CV on `CatBoostRegressor`  
   - Evaluates using **negative RMSE**

6. **Model Training & Evaluation**  
   - Trains a CatBoost model on training data  
   - Evaluates on test set using:  
     - RMSE  
     - MAE  
     - R² Score  
   - Compares performance relative to average `SettlementValue`

7. **Visualizations**  
   - Plots:  
     - Distribution of `SettlementValue`  
     - RMSE learning curves  
     - Feature importances  
     - Residuals of predictions

8. **(Optional) Feature Comparison (Commented Out)**  
   - Provides framework to compare model performance **with vs. without** a specific feature (`GeneralRest`)  
   - Side-by-side training, evaluation, and importance comparison

## Evaluation Metrics

- **RMSE (Root Mean Squared Error):** Measures average prediction error magnitude  
- **MAE (Mean Absolute Error):** Measures average absolute difference between predictions and true values  
- **R² Score:** Represents the proportion of variance in the target variable explained by the model

## Key Notes

- Log transformation helps normalize **skewed** target distributions  
- CatBoost simplifies categorical encoding — just **specify indices**  
- **Early stopping** prevents overfitting using a validation set

## How to Run

1. Ensure `Synthetic_Data_For_Students.csv` is in the same directory.  
2. Open the notebook in Jupyter or VSCode.  
3. Run all cells sequentially.  
4. Optional: Uncomment and run feature comparison block to test the impact of `GeneralRest`.

## Dependencies

```bash
pip install catboost pandas numpy scikit-learn matplotlib seaborn scipy

