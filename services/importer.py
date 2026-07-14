"""
services/importer.py
---------------------
Orchestrates the full import: for every sheet (= one product) in the
workbook, parse the title into product info, parse every parameter row,
then get-or-create the Product and each Test, and insert a Spec row
linking them.

Each sheet is committed as its own transaction: if one sheet fails, the
others are unaffected and already-processed sheets stay committed.
"""

import json

from database import crud
from database.connection import get_session
from excel.parser import parse_parameter_rows, parse_title
from excel.reader import iter_product_sheets
from utils.logger import get_logger

logger = get_logger(__name__)


def load_mapping(mapping_path: str) -> dict:
    with open(mapping_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_import(excel_path: str, mapping_path: str) -> None:
    mapping = load_mapping(mapping_path)

    header_row = mapping["header_row"]
    data_start_row = mapping["data_start_row"]
    columns_map = mapping["columns"]
    title_pattern = mapping["title_pattern"]
    test_desc_format = mapping.get("test_desc_format", "{test}: {parameter}")

    total_sheets = 0
    total_specs = 0

    for sheet_name, ws in iter_product_sheets(excel_path):
        total_sheets += 1
        session = get_session()
        try:
            product_info = parse_title(ws, title_pattern)
            logger.info(
                "Sheet '%s' -> product '%s' (ep_code=%s)",
                sheet_name, product_info.prod_name, product_info.ep_code,
            )

            product = crud.get_or_create_product(
                session,
                prod_name=product_info.prod_name,
                ep_code=product_info.ep_code,
                prod_full_name=product_info.prod_full_name,
            )

            rows = parse_parameter_rows(ws, header_row, data_start_row, columns_map)
            logger.info("Sheet '%s': %d parameter rows found", sheet_name, len(rows))

            for row in rows:
                test_desc = test_desc_format.format(
                    test=row.test or "", parameter=row.parameter
                ).strip(": ").strip()

                test = crud.get_or_create_test(session, test_desc)

                # spec_val / min / max / is_ranged / data_type intentionally left
                # blank for now, per current project stage.
                crud.create_spec(
                    session,
                    prod_id=product.id,
                    test_id=test.id,
                )
                total_specs += 1

            session.commit()
            logger.info("Sheet '%s' committed successfully.", sheet_name)

        except Exception:
            session.rollback()
            logger.exception("Sheet '%s' failed, rolled back.", sheet_name)
        finally:
            session.close()

    logger.info(
        "Import finished: %d sheet(s) processed, %d spec row(s) inserted.",
        total_sheets, total_specs,
    )
