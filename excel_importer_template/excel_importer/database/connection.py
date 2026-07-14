# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker,declarative_base
# from config import DB_URL
# engine=create_engine(DB_URL)
# SessionLocal=sessionmaker(bind=engine)
# Base=declarative_base()


from sqlalchemy import create_engine

from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)
