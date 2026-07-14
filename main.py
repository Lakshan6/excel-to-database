"""
main.py
-------
Entry point. Run with:

    python main.py
    python main.py --file data/products.xlsx
    python main.py --file data/products.xlsx --mapping mappings/column_mapping.json
"""

import argparse

import config
from services.importer import run_import


def main():
    parser = argparse.ArgumentParser(description="Import product test-spec Excel workbook into PostgreSQL.")
    parser.add_argument(
        "--file", default=config.DEFAULT_EXCEL_PATH,
        help="Path to the Excel workbook (default: data/products.xlsx)",
    )
    parser.add_argument(
        "--mapping", default=config.MAPPING_FILE_PATH,
        help="Path to column_mapping.json (default: mappings/column_mapping.json)",
    )
    args = parser.parse_args()

    run_import(excel_path=args.file, mapping_path=args.mapping)


if __name__ == "__main__":
    main()
