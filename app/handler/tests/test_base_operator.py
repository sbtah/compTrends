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
