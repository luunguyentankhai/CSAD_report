import pandas as pd
import config

class StatsReports:
    def __init__(self, process_df):
        self.Data = process_df

    def Descriptive_stats(self):

        payload = {
            "Pre": self.Data[self.Data["H1"] == 1],
            "In": self.Data[self.Data["H2"] == 1],
            "Post": self.Data[self.Data["H3"] == 1],
        }
        
        Stats_table = pd.DataFrame()

        for dummy_time, data in payload.items():
            if data.empty:
                continue

            stats = data[["CSAD_t", "R_m_t"]].agg(["mean","median","max","min","std","skew"])

            stats.loc["kurtosis"] = data[["CSAD_t", "R_m_t"]].kurt()
            stats.loc["count"] = data[["CSAD_t", "R_m_t"]].count()

            stats.index = ["Mean", "Median", "Maximum", "Minimum", "Std. Dev.", "Skewness", "Kurtosis", "Observations"]

            stats.columns = pd.MultiIndex.from_product([[dummy_time], ["CSAD_t", "R_m_t"]])


            if Stats_table.empty:
                Stats_table = stats
            else:
                Stats_table = pd.concat([Stats_table, stats], axis=1)
        
        Stats_table = Stats_table.round(4)

        print(Stats_table)
        
        file_name = config.PROCESS_DATA_DIR / "Descriptive_stats.csv"
        Stats_table.to_csv(file_name, encoding="utf-8-sig")
        return Stats_table

