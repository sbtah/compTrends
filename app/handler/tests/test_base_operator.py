import pytest
from datetime import datetime
from utilities.logger import logger

from handler.logic.base_operator import BaseOperator
import pathlib


class TestBaseOperator:
    """
    Test cases for BaseOperator.
    """

    def test_class_constructor(self):
        """Test for initializing a BaseOperator class."""

        operator = BaseOperator()

        assert isinstance(operator, BaseOperator) is True
        assert operator.time_started.strftime(
            operator.MONTH_DATE_FORMAT
        ) == datetime.today().strftime(operator.MONTH_DATE_FORMAT)
        assert isinstance(operator.BASE_DIR, pathlib.PosixPath) is True
        assert isinstance(operator.DATA_ROOT_DIR, pathlib.PosixPath) is True
        assert operator.BASE_DIR / "data" == operator.DATA_ROOT_DIR
        assert operator.DAY_DATE_FORMAT == "%d-%m-%Y"
        assert operator.MONTH_DATE_FORMAT == "%m-%Y"
        assert operator.YEAR_DATE_FORMAT == "%Y"

    def test_date_properties(self):
        """Test that:
        - current_day_month_year,
        - current_month_year,
        - current_year,
        properties returns properly formated strings."""

        operator = BaseOperator()

        assert datetime.today().strftime("%d-%m-%Y") == operator.current_day_month_year
        assert datetime.today().strftime("%m-%Y") == operator.current_month_year
        assert datetime.today().strftime("%Y") == operator.current_year
