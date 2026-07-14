"""
database/models.py
-------------------
ORM models mirroring the existing PostgreSQL tables (schema: ate).

All three `id` columns are GENERATED ALWAYS AS IDENTITY in the database,
so we map them with SQLAlchemy's Identity() construct and NEVER set `id`
manually when creating rows. Postgres generates the value and SQLAlchemy
retrieves it via RETURNING right after INSERT.
"""

from sqlalchemy import Boolean, Column, Float, ForeignKey, Identity, Integer, String
from sqlalchemy.orm import declarative_base, relationship

import config

Base = declarative_base()

SCHEMA = config.DB_SCHEMA


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, Identity(always=True), primary_key=True)
    prod_name = Column(String)
    prod_full_name = Column(String)
    ep_code = Column(String)

    specs = relationship("Spec", back_populates="product")


class Test(Base):
    __tablename__ = "test"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, Identity(always=True), primary_key=True)
    test_desc = Column(String)

    specs = relationship("Spec", back_populates="test")


class Spec(Base):
    __tablename__ = "spec"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, Identity(always=True), primary_key=True)
    spec_val = Column(String)
    min = Column(Float)
    max = Column(Float)
    prod_id = Column(Integer, ForeignKey(f"{SCHEMA}.product.id"))
    test_id = Column(Integer, ForeignKey(f"{SCHEMA}.test.id"))
    is_ranged = Column(Boolean)
    data_type = Column(String)

    product = relationship("Product", back_populates="specs")
    test = relationship("Test", back_populates="specs")
