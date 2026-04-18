import pandas as pd
from scripts import Collectdata
from pathlib import Path
import statsmodels.api as sm
import numpy as np
import config


class OLS_Analyzer:
    def __init__(self, process_df):
        self.Data = process_df
        self.result = {}

    def _prepare_data(self, data):
        X = data[["Abs_R_m_t", "R_m_t^2"]]
        Y = data["CSAD_t"]
        X = sm.add_constant(X)
        return Y, X

    def sub_sample_OLS(self):
        payload = {
            "Pre": self.Data[self.Data["H1"] == 1],
            "In": self.Data[self.Data["H2"] == 1],
            "Post": self.Data[self.Data["H3"] == 1],
        }

        for name, data in payload.items():
            if not data.empty:
                Y, X = self._prepare_data(data)
                model = sm.OLS(Y, X).fit()
                print(f"\n--- Giai đoạn: {name} ---")

                print(model.summary())
                result = {
                    "Hệ số(coef)": model.params,
                    "Sai số(std err)": model.bse,
                    "T-Statistics": model.tvalues,
                    "P_Value": model.pvalues,
                    "R^2": model.rsquared,
                    "Adj. R^2": model.rsquared_adj,
                }

                df_result = pd.DataFrame(result)
                df_result = df_result.round(5)
                file_name = f"{name}_market.csv"
                df_result.to_csv(config.PROCESS_DATA_DIR / file_name, encoding="utf-8-sig")
                self.result[name] = model
        return self.result

    def interaction_OLS(self):
        self.Data["H2_Sq_Rmt"] = self.Data["H2"] * self.Data["R_m_t^2"]
        self.Data["H3_Sq_Rmt"] = self.Data["H3"] * self.Data["R_m_t^2"]

        Y = self.Data["CSAD_t"]
        X = self.Data[["Abs_R_m_t", "R_m_t^2", "H2_Sq_Rmt", "H3_Sq_Rmt"]]

        X = sm.add_constant(X)

        model_full = sm.OLS(Y, X).fit()

        print("FULL MODEL \n")

        result = {
            "Hệ số(coef)": model_full.params,
            "Sai số(std err)": model_full.bse,
            "T-Statistics": model_full.tvalues,
            "P_Value": model_full.pvalues,
            "R^2": model_full.rsquared,
            "Adj. R^2": model_full.rsquared_adj,
        }

        df_res = pd.DataFrame(result)
        df_res = df_res.round(5)
        file_name = "Full_Market.csv"

        df_res.to_csv(config.PROCESS_DATA_DIR / file_name, encoding="utf-8-sig")
        print(model_full.summary())

        print(f"\n{'='*50}")
        return model_full
