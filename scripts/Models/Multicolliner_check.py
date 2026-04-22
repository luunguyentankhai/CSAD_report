import pandas as pd
import config
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

class MulticollinerCheck:
    def __init__(self, process_df):
        self.Data = process_df

    def Multicolliner_report(self):
        payload = {
                "Pre": self.Data[self.Data["H1"] == 1],
                "In": self.Data[self.Data["H2"] == 1],
                "Post": self.Data[self.Data["H3"] == 1],
                }


        target_vars = ["Abs_R_m_t", "R_m_t^2"]

        for time, data in payload.items():
            X = data[target_vars]

            X_ortho = sm.add_constant(X["Abs_R_m_t"])
            Y_ortho = X["R_m_t^2"]

            model_ortho = sm.OLS(Y_ortho,X_ortho).fit()

            X["R_m_t^2"] = model_ortho.resid

            corr_matrix = X.corr().round(4)

            file_corr_matrix = config.PROCESS_DATA_DIR / f"correlation_matrix_{time}.csv"
            corr_matrix.to_csv(file_corr_matrix, encoding="utf-8-sig")
            
            print(f"{'='*50}")
            print(time)
            print(corr_matrix)
            print(f"{'='*50}")
            
            X_with_const = sm.add_constant(X)

            vif_data = pd.DataFrame()

            vif_data["Dep_vars"] = X_with_const.columns

            vif_data["VIF"] = [
                    variance_inflation_factor(X_with_const.values, i)
                    for i in range(len(X_with_const.columns))
                    ]

            vif_data = vif_data.round(4)

            file_vif_data = config.PROCESS_DATA_DIR / f"vif_scores_{time}.csv"
            vif_data.to_csv(file_vif_data,index=False, encoding="utf-8-sig")

            print(vif_data)

            print(f"{'='*50}")
        return corr_matrix, vif_data
