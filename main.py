#Import libraries
import subprocess#to execute cli commands inside Python script
import multiprocessing
from pathlib import Path

#Specifying paths where relevant Python scripts reside
download_excel_path = str(Path(__file__).parent/'download_excel.py')
format_excel_path = str(Path(__file__).parent/'excel_formatting.py')


def get_data(region):
    subprocess.call(["python", download_excel_path, region])

def format_excel():
    """Adding columns date and region_code to all saved excel files"""
    subprocess.call(["python", format_excel_path])


p_sev = multiprocessing.Process(target=get_data, args=["Город Севастополь"])
p_krym = multiprocessing.Process(target=get_data, args=["Республика Крым"])

if __name__ == '__main__':
    p_sev.start()
    p_krym.start()
    p_sev.join()
    p_krym.join()
    format_excel()

