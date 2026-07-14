"""
database/crud.py
-----------------
Thin data-access layer. Every function takes an active SQLAlchemy Session
so the caller controls the transaction boundary (commit/rollback).
"""

from typing import Optional

from sqlalchemy import select

from database.models import Product, Spec, Test


def get_or_create_product(
    session,
    prod_name: str,
    ep_code: Optional[str],
    prod_full_name: Optional[str] = None,
) -> Product:
    """
    Look up a product by ep_code (preferred, since it should be unique)
    falling back to prod_name if ep_code is missing. Create it if not found.
    """
    product = None

    if ep_code:
        product = session.execute(
            select(Product).where(Product.ep_code == ep_code)
        ).scalar_one_or_none()

    if product is None:
        product = session.execute(
            select(Product).where(Product.prod_name == prod_name)
        ).scalar_one_or_none()

    if product is None:
        product = Product(
            prod_name=prod_name,
            prod_full_name=prod_full_name or prod_name,
            ep_code=ep_code,
        )
        session.add(product)
        session.flush()  # populates product.id via RETURNING, no commit yet

    return product


def get_or_create_test(session, test_desc: str) -> Test:
    """Look up a test by its description, creating it if not found."""
    test = session.execute(
        select(Test).where(Test.test_desc == test_desc)
    ).scalar_one_or_none()

    if test is None:
        test = Test(test_desc=test_desc)
        session.add(test)
        session.flush()

    return test


def create_spec(
    session,
    prod_id: int,
    test_id: int,
    spec_val: Optional[str] = None,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    is_ranged: Optional[bool] = None,
    data_type: Optional[str] = None,
) -> Spec:
    """Insert a new spec row linking a product to a test."""
    spec = Spec(
        prod_id=prod_id,
        test_id=test_id,
        spec_val=spec_val,
        min=min_val,
        max=max_val,
        is_ranged=is_ranged,
        data_type=data_type,
    )
    session.add(spec)
    return spec
