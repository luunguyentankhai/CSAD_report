from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_URL = BASE_DIR / "data"

PROCESS_DATA_DIR = DATA_URL / "processed"

RAW_DATA_DIR = DATA_URL / "raw"

BASE_URL = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol=VNINDEX&StartDate=&EndDate=&PageIndex=1&PageSize=4000"

ROOT_DATA_FILE = RAW_DATA_DIR / "Data.csv"