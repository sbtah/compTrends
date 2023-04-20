import os
import pathlib
from datetime import datetime

import pytest
from handler.logic.base_operator import BaseOperator


@pytest.fixture
def sample_directory():
    os.mkdir("test")
    directory = pathlib.PosixPath("test")
    yield directory
    os.removedirs(directory)


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

    def test_find_directory_returns_error_without_proper_path(self, caplog):
        """
        Test that find_directory returns error,
        if directory is not an instance of PosixPath.
        """

        operator = BaseOperator()
        directory = "/wrong/directory"
        returns = operator.find_directory(directory=directory)

        assert returns is None
        assert (
            f"Wrong directory provided. Received: {type(directory)}, should be path."
            in caplog.text
        )

    def test_find_directory_exists(self, caplog, sample_directory):
        """Test find_directory returs path to directory if successful."""

        operator = BaseOperator()
        directory = sample_directory
        returns = operator.find_directory(directory=directory)

        assert isinstance(returns, pathlib.PosixPath) is True
        assert "Specified directory was found." in caplog.text

    def test_find_directory_does_not_exists(self, caplog):
        """Test find_directory returs None when directory does not exist."""

        operator = BaseOperator()
        directory = pathlib.PosixPath("test")
        returns = operator.find_directory(directory=directory)

        assert returns is None
        assert "Specified directory does not exists." in caplog.text

    def test_find_directory_raises_exception(self):
        """Test that find_directory raises exception."""

        operator = BaseOperator()
        with pytest.raises(Exception) as context:
            output = operator.find_directory()

    def test_create_directory_returns_error_without_proper_path(self, caplog):
        """
        Test that create_directory returns error,
        if directory is not an instance of PosixPath.
        """

        operator = BaseOperator()
        directory = "/wrong/directory"
        returns = operator.create_directory(directory=directory)

        assert returns is None
        assert (
            f"Wrong directory provided. Received: {type(directory)}, should be path."
            in caplog.text
        )

    def test_create_directory_successful(self, caplog):
        """Test that create_directory creates proper directory."""

        operator = BaseOperator()
        directory = pathlib.PosixPath("test")
        returns = operator.create_directory(directory=directory)

        assert returns is True
        assert f"Created directory: '{directory}'." in caplog.text
        assert os.path.exists(directory) is True
        os.removedirs(directory)
