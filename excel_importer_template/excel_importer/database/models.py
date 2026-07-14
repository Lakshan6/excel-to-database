from sqlalchemy import Column,Integer,String,Float,Boolean,ForeignKey
from .connection import Base
class Product(Base):
 __tablename__="product";__table_args__={"schema":"ate"}
 id=Column(Integer,primary_key=True);prod_name=Column(String);prod_full_name=Column(String);ep_code=Column(String)
class Test(Base):
 __tablename__="test";__table_args__={"schema":"ate"}
 id=Column(Integer,primary_key=True);test_desc=Column(String)
class Spec(Base):
 __tablename__="spec";__table_args__={"schema":"ate"}
 id=Column(Integer,primary_key=True);spec_val=Column(String);min=Column(Float);max=Column(Float);prod_id=Column(Integer,ForeignKey("ate.product.id"));test_id=Column(Integer,ForeignKey("ate.test.id"));is_ranged=Column(Boolean);data_type=Column(String)
