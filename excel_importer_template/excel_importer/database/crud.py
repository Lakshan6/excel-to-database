from .models import Product,Test,Spec
from sqlalchemy import select

def get_or_create_product(db,name,ep):
 p=db.scalar(select(Product).where(Product.prod_name==name))
 if p:return p.id
 p=Product(prod_name=name,prod_full_name=name,ep_code=ep);db.add(p);db.flush();return p.id

def get_or_create_test(db,desc):
 t=db.scalar(select(Test).where(Test.test_desc==desc))
 if t:return t.id
 t=Test(test_desc=desc);db.add(t);db.flush();return t.id

def insert_spec(db,pid,tid):
 db.add(Spec(prod_id=pid,test_id=tid))
