import pandas as pd
from scripts import Collectdata
import time
import config


class Processed:
    def __init__(self):
        self.Data_map = Collectdata.Data_Harvester().Data_map

    def GetDate(self):
        for k in self.Data_map.keys():
            for v in self.Data_map[k]:
                start_time = time.perf_counter()
                try:
                    set_dir = config.RAW_DATA_DIR / f"{k}" / f"{v}.csv"
                    df = pd.read_csv(set_dir)

                    df["Ngay"] = pd.to_datetime(
                        df["Ngay"], format="%d/%m/%Y", errors="coerce"
                    )

                    df = df.dropna(subset=["Ngay"])

                    start_dt = pd.to_datetime("01/01/2019", format="%d/%m/%Y")
                    end_dt = pd.to_datetime("01/01/2024", format="%d/%m/%Y")

                    mask = (df["Ngay"] >= start_dt) & (df["Ngay"] <= end_dt)
                    df_filter = df.loc[mask]

                    if len(df_filter) > 0:
                        df_filter["Ngay"] = df_filter["Ngay"].dt.strftime("%d/%m/%Y")
                        df_filter.to_csv(set_dir, index=False, encoding="utf-8-sig")
                except Exception as e:
                    print(f"Error : {e}")
                finally:
                    end_time = time.perf_counter()
                    total_time = end_time - start_time
                    print(f"Lọc mã {v} trong {total_time:.4f} giây")
