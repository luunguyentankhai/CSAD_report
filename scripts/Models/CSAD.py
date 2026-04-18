from pathlib import Path
import pandas as pd
import numpy as np
from scripts import Collectdata
from time import perf_counter
import config


class CSAD:
    def __init__(self):
        self.collectdata = Collectdata.Data_Harvester()
        self.Raw_Data = config.RAW_DATA_DIR
        self.finally_df = None

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
                df["R_i_t"] = np.log(df["GiaDongCua"] / df["GiaDongCua"].shift(1)) * 100

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

    def Covid_dummy_variabel(self):
        start_pre_covid = "01/01/2019"
        end_pre_covid = "31/01/2020"

        start_in_covid = "01/02/2020"
        end_in_covid = "31/03/2022"

        start_post_covid = "01/04/2022"
        end_post_covid = "01/01/2024"

        start_date = "01/01/2019"
        end_date = "01/01/2024"

        rit = self.R_i_t(start_date, end_date)

        if not rit.empty:
            rmt = self.R_m_t(rit)
            final_df = self.Final_Regression_Data(rmt)

            H1 = (
            final_df["Ngay"] >= pd.to_datetime(start_pre_covid, format="%d/%m/%Y")
            ) & (final_df["Ngay"] <= pd.to_datetime(end_pre_covid, format="%d/%m/%Y"))
            H2 = (final_df["Ngay"] >= pd.to_datetime(start_in_covid, format="%d/%m/%Y")) & (
                final_df["Ngay"] <= pd.to_datetime(end_in_covid, format="%d/%m/%Y")
            )
            H3 = (
                final_df["Ngay"] >= pd.to_datetime(start_post_covid, format="%d/%m/%Y")
            ) & (final_df["Ngay"] <= pd.to_datetime(end_post_covid, format="%d/%m/%Y"))


            final_df["H1"] = np.where(H1, 1, 0)
            final_df["H2"] = np.where(H2, 1, 0)
            final_df["H3"] = np.where(H3, 1, 0)
        
        self.finally_df = final_df

        return self.finally_df
        