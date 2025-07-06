from datetime import date


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
        return "First date is not valid"
    if not isinstance(d2, date):
        return "Second date is not valid"
    return abs((d2 - d1).days)
