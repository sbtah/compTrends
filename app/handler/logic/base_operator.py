import os
import pathlib
from datetime import datetime
from typing import Union

import pandas as pd
from handler.settings import BASE_DIR, DATA_ROOT_DIR
from utilities.logger import logger


class BaseOperator:
    BASE_DIR = BASE_DIR
    DATA_ROOT_DIR = DATA_ROOT_DIR

    DAY_DATE_FORMAT = "%d-%m-%Y"
    MONTH_DATE_FORMAT = "%m-%Y"
    YEAR_DATE_FORMAT = "%Y"

    def __init__(self):
        self.logger = logger
        self.time_started = datetime.today()

    @property
    def current_day_month_year(self) -> str:
        return self.time_started.strftime(self.DAY_DATE_FORMAT)

    @property
    def current_month_year(self) -> str:
        return self.time_started.strftime(self.MONTH_DATE_FORMAT)

    @property
    def current_year(self) -> str:
        return self.time_started.strftime(self.YEAR_DATE_FORMAT)

    def find_directory(
        self, directory: pathlib.PosixPath
    ) -> Union[pathlib.PosixPath, None]:
        """
        Searches for specified directory.
        Return directory path if successful.
        - :arg directory: Desired path.
        """
        if isinstance(directory, pathlib.PosixPath):
            try:
                check = os.path.exists(directory)
                if check:
                    self.logger.info("Specified directory was found.")
                    return directory
                else:
                    self.logger.info("Specified directory does not exists.")
                    return check
            except Exception as e:
                self.logger.error(f"(find_directory) Some other exception: {e}")
                raise
        else:
            self.logger.error(
                f"Wrong directory provided. Received: {type(directory)}, should be path."
            )
            return None

    def create_directory(self, directory: pathlib.PosixPath):
        """
        Creates directory for specified path.
        """
        if isinstance(directory, pathlib.PosixPath):
            try:
                os.mkdir(directory)
                self.logger.info(f"Created directory: '{directory}'.")
                return True
            except FileExistsError:
                self.logger.info(f"Specified directory exists. Passing...")
                return None
            except Exception as e:
                self.logger.error(f"(create_directory) some other exception: {e}")
                raise
        else:
            self.logger.error(
                f"Wrong directory provided. Received: {type(directory)}, should be path."
            )
            return None

    def search_directory_for_file(
        self,
        directory: pathlib.PosixPath,
        filename: str,
    ):
        """
        Searches for a file in specified directory.
        Returns a path to a file if successful.
        """
        if isinstance(directory, pathlib.PosixPath):
            list_dir = os.listdir(directory)
            for file in list_dir:
                if filename == file:
                    self.logger.info(f"Found directory for a file: {filename}")
                    return directory / file
                else:
                    self.logger.error(
                        f"Cannot find {filename} in {directory} directory."
                    )
                    return None
        else:
            self.logger.error(
                f"Wrong directory provided. Received: {type(directory)}, should be path."
            )
            return None

    def open_xlsx_file(self, directory: pathlib.PosixPath) -> pd.DataFrame:
        """
        Open specified file in provided directory.
        Uses pandas library, returns DataFrame object.
        """
        if isinstance(directory, pathlib.PosixPath):
            try:
                frame = pd.read_excel(directory)
                return frame
            except FileNotFoundError:
                self.logger.error("Specified xlsx file was not found.")
                return None
            except Exception as e:
                self.logger.error(
                    f"(open_xlsx_file_for_date) Some other exception: {e}"
                )
                return None
        else:
            self.logger.error(
                f"Wrong directory provided. Received: {type(directory)}, should be path."
            )
            return None
