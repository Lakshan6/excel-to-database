# Excel → PostgreSQL Importer

Imports a multi-sheet Excel workbook (one sheet per product test-report
template) into the `ate.product`, `ate.test`, and `ate.spec` tables.

## What it does

For every sheet in the workbook:

1. **Row 1** holds a title like `product abc EP Code 123456789`. It's split
   into `prod_name` (`"product abc"`) and `ep_code` (`"123456789"`) using
   the regex in `mappings/column_mapping.json`.
2. **Row 2** holds the headers (`S.No.`, `Test`, `Parameter`,
   `Observation/ Observed Value`, `If Not Satisfactory/...`). The importer
   locates each column by name, so it doesn't matter which column letter
   they're actually in.
3. **Row 3 onward**: `S.No.` and `Test` are merged across several rows in
   the source sheet (e.g. `Visual Test` spans 1.1–1.5). openpyxl only puts
   a value in the top-left cell of a merge, so the importer **forward-fills**
   both columns as it reads down.
4. For each row that has a `Parameter` value, it builds a `test_desc`
   (default: `"<Test>: <Parameter>"`, e.g. `"Visual Test: 1.1 Broken"`).
5. **Get-or-create** is used for both `Product` (matched by `ep_code`, then
   `prod_name`) and `Test` (matched by `test_desc`) — so re-running the
   import, or importing a second workbook that shares products/tests,
   won't create duplicates.
6. A `Spec` row is inserted linking `prod_id` + `test_id`. Only the ids are
   stored in `spec` — `spec_val`, `min`, `max`, `is_ranged`, and
   `data_type` are left `NULL` at this stage (per current project plan;
   these get populated in a later phase from the parameter text itself).

Each **sheet is its own transaction** — if one sheet fails to parse, the
others still commit, and the error is written to `logs/import.log`.

## Folder structure

```
excel_importer/
├── main.py                    # entry point
├── config.py                  # DB connection + file paths (env-var driven)
├── requirements.txt
├── data/
│   └── products.xlsx          # <- put your workbook here
├── mappings/
│   └── column_mapping.json    # header names, title regex, test_desc format
├── database/
│   ├── connection.py          # SQLAlchemy engine/session
│   ├── models.py              # Product, Test, Spec ORM models
│   └── crud.py                # get_or_create_product/test, create_spec
├── excel/
│   ├── reader.py              # opens the workbook (openpyxl)
│   └── parser.py              # title parsing + forward-fill logic
├── services/
│   └── importer.py            # orchestrates the whole run
├── utils/
│   └── logger.py
└── logs/
    └── import.log             # created on first run
```

## Setup

1. **Install dependencies** (already done on your machine per your message,
   but for reference):

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the DB connection.** Either edit the defaults in `config.py`,
   or export environment variables before running:

   ```bash
   export DB_USER=postgres
   export DB_PASSWORD=yourpassword
   export DB_HOST=localhost
   export DB_PORT=5432
   export DB_NAME=your_database
   export DB_SCHEMA=ate
   ```

3. **Make sure the tables exist** (run your existing DDL — `product`,
   `spec`, `test` in the `ate` schema, all with `id` as
   `GENERATED ALWAYS AS IDENTITY`, which is what you already set up).

4. **Drop your workbook** into `data/products.xlsx` (or point `--file` at
   wherever it lives).

## Running it

```bash
python main.py
# or explicitly:
python main.py --file data/products.xlsx --mapping mappings/column_mapping.json
```

Progress and any errors are printed to the console and appended to
`logs/import.log`.

## Adjusting the template layout

If a workbook's headers, title format, or `test_desc` naming differ,
you don't need to touch any code — edit `mappings/column_mapping.json`:

- `header_row` / `data_start_row` — which rows headers/data start on.
- `columns` — the exact header text for each logical field (whitespace
  and casing are normalized automatically, so `"Test"` and `" test "`
  both match).
- `title_pattern` — a regex with named groups `prod_name` and `ep_code`.
- `test_desc_format` — a Python `.format()` string using `{test}` and
  `{parameter}`.

## Notes / open items for the next phase

- `prod_full_name` currently defaults to the same value as `prod_name`
  (the title row only gives one name). Update `excel/parser.py` /
  `services/importer.py` if a separate full name becomes available.
- `spec_val`, `min`, `max`, `is_ranged`, `data_type` are all `NULL` after
  this import — per your notes, a later phase will parse `min`/`max` out
  of the parameter text, derive `is_ranged`, and set `data_type` to one
  of `degreeminseconds`, `boolean`, or `integer`.
- The `Login 1` / `Login 2` column (leftmost, in your screenshot) isn't
  currently stored anywhere, since the `spec` table has no column for it.
  Flag if that needs to be captured.
