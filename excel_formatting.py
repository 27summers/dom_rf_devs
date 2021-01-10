#Importing libraries
import pandas as pd
from pathlib import Path
import re 
import datetime

print(f'The execution of script "{__file__}" has started')


file_path = Path(__file__).parent
excel_files_path = file_path/'excel_files'

excel_files = list(excel_files_path.glob('*.xlsx'))

#Adding date and region_code columns to all excel files
for i in range(len(excel_files)):
    date = re.findall('\d{2}-\d{2}-\d{4}', str(excel_files[i])) 
    date_obj = datetime.datetime.strptime(date[0],'%d-%m-%Y')
    region_code = re.findall('\d{2}(?=_)', str(excel_files[i])) #(?=_) followed by '_' character but not part of output
    df = pd.read_excel(excel_files[i], skipfooter=1, skiprows=3)
    if 'date' in df.columns:
        pass
    else:
        df['date'] = date_obj
    if 'region_code' in df.columns:
        pass
    else:
        df['region_code'] = region_code[0]
    df.to_excel(excel_files[i])

#Removing 'garbage' from the data
df = pd.concat([pd.read_excel(excel_file, index_col=[0]) for excel_file in excel_files])
records_2_remove = df[(df['Девелопер']=='Итого') | (df['Девелопер']==1)].index.to_list()

final_df = df[~df.index.isin(list(set(records_2_remove)))] 


"""In the future the line saving final_df as Excel File will be replaced with a code transferring 
data from the dataframe to newly created table in an Oracle database"""

#Saving final dataframe into Excel (for now)
final_df.to_excel(file_path/'developers_data_sev_and_crimea.xlsx')
