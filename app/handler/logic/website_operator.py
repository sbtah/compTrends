from handler.logic.base_operator import BaseOperator
import pathlib


class WebsiteOperator(BaseOperator):
    """
    Website operator.
    """

    def __init__(self, website, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.website = website
        self.logger.info(f"Started operator for : '{self.website} '")

    @property
    def website_directory(self):
        if self.website is not None:
            return self.DATA_ROOT_DIR / self.website
        else:
            return self.DATA_ROOT_DIR

    @property
    def current_month_rapport_pattern(self):
        return f"{self.website}-{self.current_month_year}.xlsx"

    def find_directory_for_website(self, website) -> bool:
        """
        Searches for specified website directory in data folder.
        Return directory path if successful.
        """
        website_directory = self.DATA_ROOT_DIR / website
        return self.find_directory(directory=website_directory)

    def create_directory_for_website(self, website: str):
        """
        Creates directory for website in data directory,
        where all rapports will be stored.
        """
        website_directory = self.DATA_ROOT_DIR / website
        return self.create_directory(directory=website_directory)

    def search_website_directory_for_file(self, filename: str):
        """"""
        path = self.search_directory_for_file(
            directory=self.website_directory,
            filename=filename,
        )
        return path

    def search_website_directory_for_current_rapport(self):
        """"""
        path = self.search_directory_for_file(
            directory=self.website_directory,
            filename=self.current_month_rapport_pattern,
        )
        return path

    def create_xlsx_rapport_for_website(self):
        """"""
        rapport = self.create_xlsx_file_for_date(
            directory=self.website_directory,
            filename=self.current_month_rapport_pattern,
        )
        return rapport
