from pathlib import Path
import os
import requests
import pandas as pd
import time
import config


class Data_Harvester:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.df = pd.read_csv(config.ROOT_DATA_FILE)
        self.Data_map = self.df.groupby('Sector')['Ticker'].apply(list).to_dict()
    
    def Harvester(self):
        # Using for company
        for k in self.Data_map.keys():
            if Path.exists(config.RAW_DATA_DIR / k):
                print('folder có tồn tại')
                pass
            else:
                print('folder không tồn tại... đang tạo folder')
                os.mkdir(config.RAW_DATA_DIR / k)
            for v in self.Data_map[k]:
                if Path.exists(config.RAW_DATA_DIR / k / f"{v}.csv"):
                    print("file dữ liệu đã tồn tại")
                    continue
                else:
                    try:
                        print("Bắt đầu quá trình tải dữ liệu")
                        start_time = time.perf_counter()
        
                        self.base_url = f"https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol={v}&StartDate=&EndDate=&PageIndex=1&PageSize=4000"
                        response = requests.get(self.base_url)

                        response.raise_for_status()

                        raw_data = response.json()
                        
                        stock_ticker = raw_data["Data"]["Data"]

                        df = pd.DataFrame(stock_ticker)
                        df_selected = df[["Ngay", "Symbol", "GiaDongCua"]]

                        csv_name = f"{v}.csv"
                        df_selected.to_csv(config.RAW_DATA_DIR / k / csv_name, index=False, encoding="utf-8-sig")
                    except Exception as e:
                        print(f"Error : {e}")
                    finally:
                        end_time = time.perf_counter()
                        total_time = end_time - start_time
                        print(f"Đã tải mã {v} trong {total_time:.4f} giây")