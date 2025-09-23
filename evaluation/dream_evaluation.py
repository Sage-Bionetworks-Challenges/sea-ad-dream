# import anndata as ad
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import (
    cohen_kappa_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

discrete_metrics = ["Braak", "Thal", "ADNC", "CERAD"]
continous_metrics = ["6e10", "AT8", "NeuN", "GFAP"]
ordinal_regression_order = {
    "Braak": [
        "Braak 0",
        "Braak I",
        "Braak II",
        "Braak III",
        "Braak IV",
        "Braak V",
        "Braak VI",
    ],
    "Thal": ["Thal 0", "Thal 1", "Thal 2", "Thal 3", "Thal 4", "Thal 5"],
    "ADNC": ["Not AD", "Low", "Intermediate", "High"],
    "CERAD": ["Absent", "Sparse", "Moderate", "Frequent"],
}


def concordance_correlation_coefficient(y_true, y_pred):
    """Calculates Lin's Concordance Correlation Coefficient."""
    mean_true = np.mean(y_true)
    mean_pred = np.mean(y_pred)
    var_true = np.var(y_true)
    var_pred = np.var(y_pred)
    cov_true_pred = np.cov(y_true, y_pred, bias=True)[0, 1]

    ccc = (2 * cov_true_pred) / (var_true + var_pred + (mean_true - mean_pred) ** 2)
    return ccc


def goal1_evaluation(df_adata, df):
    dict_performance = {}
    for i in discrete_metrics:
        dict_discrete = {}
        count = 0
        for j in ordinal_regression_order[i]:
            dict_discrete[j] = count
            count = count + 1
        df_adata["num_" + i] = df_adata[i].map(dict_discrete)
        df["num_predicted " + i] = df["predicted " + i].map(dict_discrete)
        merged_df = pd.merge(df_adata, df, left_index=True, right_index=True)
        # MAE, R2, QWK
        y_true = merged_df["num_" + i].to_numpy()
        y_pred = merged_df["num_predicted " + i].to_numpy()
        y_pred = y_pred[~np.isnan(y_true)]
        y_true = y_true[~np.isnan(y_true)]
        mae = mean_absolute_error(y_true, y_pred)
        res = stats.spearmanr(y_true, y_pred)
        r2 = res.statistic
        qwk = cohen_kappa_score(y_true, y_pred, weights="quadratic")
        dict_performance[i + "_MAE"] = mae
        dict_performance[i + "_R2"] = r2
        dict_performance[i + "_QWK"] = qwk
    return dict_performance


def goal2_evaluation(df_adata, df):
    dict_performance = {}
    for i in continous_metrics:
        # MSE, R2, CCC
        merged_df = pd.merge(df_adata, df, left_index=True, right_index=True)
        y_true = merged_df["percent " + i + " positive area"].to_numpy()
        y_pred = merged_df["predicted " + i].to_numpy()
        y_pred = y_pred[~np.isnan(y_true)]
        y_true = y_true[~np.isnan(y_true)]
        mse = mean_squared_error(y_true, y_pred)
        r2 = np.corrcoef(y_true, y_pred)[0, 1]
        ccc = concordance_correlation_coefficient(y_true, y_pred)
        dict_performance[i + "_MSE"] = mse
        dict_performance[i + "_R2"] = r2
        dict_performance[i + "_CCC"] = ccc
    return dict_performance
