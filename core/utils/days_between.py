from datetime import date
import inspect
from core.exceptions.invalid_input_exception import InvalidInput


def days_between(d1: date, d2: date):
    """
    calculate the days diff between 2 dates
    -----------------------------------------
    args:  d1: first date
    d1: second date
    -----------------------------------------
    return: an int representing the difference in days
    """
    if not isinstance(d1, date):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in function '{func_name}': d1")
    if not isinstance(d2, date):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in function '{func_name}': d2")
    return abs((d2 - d1).days)
