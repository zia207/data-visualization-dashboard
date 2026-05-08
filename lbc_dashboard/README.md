# 🫁 LBC Mortality Rate — Streamlit ML Dashboard

Interactive ML dashboard for predicting **Lung & Bronchus Cancer (LBC) mortality rates**
across US counties. Built with Streamlit — fully reproducible across any compatible dataset.

---

## Quickstart

```bash
# 1. Clone / download this folder
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

Place your CSV in the same folder **or** upload it via the sidebar file picker.

---

## Dashboard tabs

| Tab | What it does |
|-----|-------------|
| 📊 **EDA** | Distribution, correlation bars, temporal trend, scatter explorer, descriptive stats, heatmap |
| ✂️ **Data split** | Random / Temporal / Spatial / K-Fold · adjustable train/val/test sliders · visual split bar |
| 🔢 **Covariates** | Feature selection, presets, pair-plot, importance preview |
| 🤖 **Models** | 9 base models + ensemble builder (Stacking, Blending, Weighted avg, Bagging, Boosting chain) · meta-learner picker |
| 📏 **Metrics** | Choose RMSE, MAE, R², MAPE, MedAE · set ranking metric |
| 🚀 **Train & compare** | One-click training, progress bar, RMSE/R² charts, predicted vs actual, residuals, downloadable results CSV |
| 🌟 **Variable importance** | Pearson \|r\|, permutation importance, coefficient magnitude, Gini/impurity, SHAP · directional effects · cross-model heatmap · year-stability line chart |

---

## Using a different dataset

Edit only the **sidebar** (data & modelling columns) and the **Year filter** bar above the tabs — no code changes needed:

1. Upload your CSV (or rely on the default filename next to `app.py`)
2. Select **Target column**, **ID columns**, **Temporal column**
3. Choose **Feature columns**
4. Use **Year filter** (above the tabs) if your data is panel/longitudinal — it applies to every tab
5. Everything else adapts automatically

---

## Requirements

- Python ≥ 3.9
- See `requirements.txt` for all packages
- `shap` and `pygam` are optional — the app works without them
  (SHAP and GAM options are hidden when not installed)

---

## Ensemble stacking

The ensemble builder supports:

| Strategy | Description |
|----------|-------------|
| **Stacking** | Meta-learner trained on out-of-fold predictions (most flexible) |
| **Blending** | Meta-learner trained on held-out validation set (faster) |
| **Weighted averaging** | Fixed weighted mean of base model outputs |
| **Bagging** | Bootstrap aggregation — reduces variance |
| **Boosting chain** | Heterogeneous sequential residual correction |

Meta-learners: Linear Regression, Ridge, Lasso, ElasticNet, Random Forest, Gradient Boosting, Simple averaging.
