from datetime import date


def days_between(d1: date, d2: date):
        if not isinstance(d1, date):
                return "First date is not valid"
        if not isinstance(d2, date):
                return "Second date is not valid"
        return abs((d2-d1).days)
