import pandas as pd,json
from pathlib import Path
MAP=json.loads(Path("mappings/column_mapping.json").read_text())
def dataframe(path,sheet):
 df=pd.read_excel(path,sheet_name=sheet,header=1).ffill();
 return df.rename(columns=MAP)
