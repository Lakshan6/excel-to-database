from database.connection import SessionLocal
from database.crud import *
from excel.parser import workbook,product_info
from excel.transformer import dataframe

def import_workbook(path):
 wb=workbook(path)
 db=SessionLocal()
 try:
  for s in wb.sheetnames:
   ws=wb[s];name,ep=product_info(ws);pid=get_or_create_product(db,name,ep);df=dataframe(path,s)
   for _,r in df.iterrows():
    param=r.get("parameter_name")
    if not param: continue
    tid=get_or_create_test(db,str(param));insert_spec(db,pid,tid)
  db.commit();print("Import complete")
 except Exception:
  db.rollback();raise
 finally: db.close()
