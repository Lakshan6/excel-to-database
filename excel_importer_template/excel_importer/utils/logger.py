import logging

from pathlib import Path

from config import LOG_FOLDER
from config import LOG_LEVEL

LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOG_FOLDER / "import.log"

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("excel_importer")