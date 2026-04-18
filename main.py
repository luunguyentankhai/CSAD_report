from scripts import Collectdata, Processed
<<<<<<< HEAD
from scripts.Models import CSAD, OLS
=======
from scripts.Models import CSAD, OLS, Des_Sta
>>>>>>> c0bbbcd (fix and rewrite to collect data)
from time import perf_counter

class Main:
    def __init__(self):
        self.CD = Collectdata.Data_Harvester()
        self.PD = Processed.Processed()
        
        #models
        self.CSAD = CSAD.CSAD()
        self.OLS = OLS
<<<<<<< HEAD
=======
        self.DS = Des_Sta
>>>>>>> c0bbbcd (fix and rewrite to collect data)
def main():
    start = Main()
    start.CD.Harvester()
    start.PD.GetDate()
<<<<<<< HEAD
    # csad_t = start.CSAD.Covid_dummy_variabel()
    # start.OLS.OLS_Analyzer(csad_t).interaction_OLS()
    # start.OLS.OLS_Analyzer(csad_t).sub_sample_OLS()
=======
    csad_t = start.CSAD.Covid_dummy_variabel()
    start.OLS.OLS_Analyzer(csad_t).interaction_OLS()
    start.OLS.OLS_Analyzer(csad_t).sub_sample_OLS()
    start.DS.StatsReports(csad_t).Descriptive_stats()
>>>>>>> c0bbbcd (fix and rewrite to collect data)
    

if __name__ == "__main__":
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    total_time = end_time - start_time
<<<<<<< HEAD
    print(f"Tổng thời gian chạy : {total_time:.4f} giây")
=======
    print(f"Tổng thời gian chạy : {total_time:.4f} giây")
>>>>>>> c0bbbcd (fix and rewrite to collect data)
