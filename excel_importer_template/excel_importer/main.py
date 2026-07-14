# from services.importer import import_workbook
# from config import EXCEL_FILE
# if __name__=="__main__": import_workbook(EXCEL_FILE)


from utils.logger import logger

from database.session import get_db

logger.info("Starting Excel Importer")


def main():

    with get_db():

        logger.info("Database Connected Successfully")


if __name__ == "__main__":

    main()