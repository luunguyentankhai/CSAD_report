from pathlib import Path
from scripts import Collectdata, Processed, CSAD
import pandas as pd
import numpy as np
from time import perf_counter

BASE_URL = Path(__file__).resolve().parent

DATA_URL = BASE_URL / "data"


class Main:
    def Harvester(self):
        return Collectdata.Data_Harvester().Harvester()

    def GetDate(self):
        return Processed.Processed().GetDate()

    def Covid(self):
        start_time = perf_counter()

        self.Harvester()
        self.GetDate()

        start_pre_covid = "01/01/2019"
        end_pre_covid = "31/01/2020"

        start_in_covid = "01/02/2020"
        end_in_covid = "31/03/2022"

        start_post_covid = "01/04/2022"
        end_post_covid = "01/01/2024"

        processer = CSAD.CSAD()
        start_date = "01/01/2019"
        end_date = "01/01/2024"

        rit = processer.R_i_t(start_date, end_date)

        if not rit.empty:
            rmt = processer.R_m_t(rit)
            final_df = processer.Final_Regression_Data(rmt)

            H1 = (
                final_df["Ngay"] >= pd.to_datetime(start_pre_covid, format="%d/%m/%Y")
            ) & (final_df["Ngay"] <= pd.to_datetime(end_pre_covid, format="%d/%m/%Y"))
            H2 = (
                final_df["Ngay"] >= pd.to_datetime(start_in_covid, format="%d/%m/%Y")
            ) & (final_df["Ngay"] <= pd.to_datetime(end_in_covid, format="%d/%m/%Y"))
            H3 = (
                final_df["Ngay"] >= pd.to_datetime(start_post_covid, format="%d/%m/%Y")
            ) & (final_df["Ngay"] <= pd.to_datetime(end_post_covid, format="%d/%m/%Y"))

            final_df["H1"] = np.where(H1, 1, 0)
            final_df["H2"] = np.where(H2, 1, 0)
            final_df["H3"] = np.where(H3, 1, 0)

            final_df.to_csv(
                DATA_URL / "processed" / "Final.csv", index=False, encoding="utf-8-sig"
            )

            print(final_df)

        end_time = perf_counter()
        total_time = end_time - start_time
        print(f"Tổng thời gian chạy : {total_time:.4f} giây")


start = Main()
start.Covid()
