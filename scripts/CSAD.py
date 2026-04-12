from pathlib import Path
import pandas as pd
import numpy as np
from scripts import Collectdata
from time import perf_counter


class CSAD:
    def __init__(self):
        self.collectdata = Collectdata.Data_Harvester()
        self.Raw_Data = self.collectdata.Data_raw_dir

    def R_i_t(self, start_data, end_data):
        tmp_dict = self.collectdata.Data_map
        all_data = []
        for k in tmp_dict.keys():
            for v in tmp_dict[k]:
                df = pd.read_csv(self.Raw_Data / f"{k}" / f"{v}.csv")

                df["Ngay"] = pd.to_datetime(df["Ngay"], format="%d/%m/%Y")

                mask = (df["Ngay"] >= pd.to_datetime(start_data, format="%d/%m/%Y")) & (
                    df["Ngay"] <= pd.to_datetime(end_data, format="%d/%m/%Y")
                )
                df = df.loc[mask]
                df = df.sort_values(by="Ngay")

                df["Nganh"] = k
                df["MaCP"] = v
                df["R_i_t"] = np.log(df["GiaDongCua"] / df["GiaDongCua"].shift(1))

                all_data.append(df)
        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)
            final_df = final_df.dropna(subset=["R_i_t"])
            return final_df

        return pd.DataFrame()

    def R_m_t(self, df):
        df["R_m_t"] = df.groupby(["Ngay"])["R_i_t"].transform("mean")
        return df

    def Final_Regression_Data(self, df):
        df["Abs_Dev"] = np.abs(df["R_i_t"] - df["R_m_t"])

        final_df = (
            df.groupby(["Ngay"])
            .agg(CSAD_t=("Abs_Dev", "mean"), R_m_t=("R_m_t", "first"))
            .reset_index()
        )

        final_df["Abs_R_m_t"] = np.abs(final_df["R_m_t"])
        final_df["R_m_t^2"] = final_df["R_m_t"] ** 2

        return final_df



