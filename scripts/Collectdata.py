from pathlib import Path
import os
import requests
import pandas as pd
import time


class Data_Harvester:
    def __init__(self):
        self.base_url = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol=VNINDEX&StartDate=&EndDate=&PageIndex=1&PageSize=4000"
        self.Curr_dir = Path(__file__).resolve().parent
        self.Data_raw_dir = self.Curr_dir.parent / "data" / "raw"
        self.Data_download = self.Curr_dir.parent / "data" / "processed"
        self.df = pd.read_csv(self.Data_raw_dir / "Data.csv")
        self.Data_map = self.df.groupby('Sector')['Ticker'].apply(list).to_dict()
    
    def Harvester(self):
        # Using for company            
        for k in self.Data_map.keys():
            if Path.exists(self.Data_raw_dir / k):
                print('folder có tồn tại')
                pass
            else:
                print('folder không tồn tại... đang tạo folder')
                os.mkdir(self.Data_raw_dir / k)
            for v in self.Data_map[k]:
                if Path.exists(self.Data_raw_dir / k / f"{v}.csv"):
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
                        df_selected = df[["Ngay", "GiaDongCua"]]

                        csv_name = f"{v}.csv"
                        df_selected.to_csv(self.Data_raw_dir / k / csv_name, index=False, encoding="utf-8-sig")
                    except Exception as e:
                        print(f"Error : {e}")
                    finally:
                        end_time = time.perf_counter()
                        total_time = end_time - start_time
                        print(f"Đã tải mã {v} trong {total_time:.4f} giây")