from scripts import Collectdata, Processed
from scripts.Models import CSAD, OLS, Des_Sta, Multicolliner_check
from time import perf_counter

class Main:
    def __init__(self):
        self.CD = Collectdata.Data_Harvester()
        self.PD = Processed.Processed()
        
        #models
        self.CSAD = CSAD.CSAD()
        self.OLS = OLS
        self.DS = Des_Sta
        self.MC = Multicolliner_check
def main():
    start = Main()
    start.CD.Harvester()
    start.PD.GetDate()  
    csad_t = start.CSAD.Covid_dummy_variabel()
    start.MC.MulticollinerCheck(csad_t).Multicolliner_report()
    start.OLS.OLS_Analyzer(csad_t).interaction_OLS()
    start.DS.StatsReports(csad_t).Descriptive_stats()
    start.OLS.OLS_Analyzer(csad_t).sub_sample_OLS()

if __name__ == "__main__":
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    total_time = end_time - start_time
    print(f"Tổng thời gian chạy : {total_time:.4f} giây")

