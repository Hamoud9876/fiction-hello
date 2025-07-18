from core.data.data import male_first_names
from core.data.data import last_names
from core.data.data import male_middle_names
from core.data.data import female_first_names
from core.data.data import female_middle_names
from random import randint
from datetime import date
from core.exceptions.invalid_input_exception import InvalidInput
from faker import Faker
import inspect


def generate_customers_data(value: int):
    """
    creates a random customers details
    -----------------------------------------
    args: "value" represent how many customer
    to be created
    -----------------------------------------
    return: a list containing of customers
    """

    if not isinstance(value, int):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in '{func_name}': value")

    customers = []
    for i in range(1, value + 1):
        # pick a random gender
        gender = randint(0, 2)
        treat_as = None

        if gender == 2:
            treat_as = randint(0, 1)

        # if gender is male or treat as is 0
        # the details will be picked from the male list
        # otherwise it will come from the females details
        if gender == 0 or treat_as == 0:
            random_num = randint(0, 99)
            first_name = male_first_names[random_num]

            has_second_name = randint(0, 99)
            if has_second_name < 40:
                random_num = randint(0, 99)
                middle_name = male_middle_names[random_num]
            else:
                middle_name = None

            random_num = randint(0, 199)
            last_name = last_names[random_num]

            fake = Faker()

            end_date = date(year=2007, month=6, day=26)
            if treat_as:
                start_date = date(year=1970, month=1, day=1)
            else:
                start_date = "-80y"
            birthdate = fake.date_between(start_date, end_date)

            join_date = fake.date_between(start_date="-15y", end_date="now")
        else:
            random_num = randint(0, 99)
            first_name = female_first_names[random_num]

            has_second_name = randint(0, 99)
            if has_second_name < 40:
                random_num = randint(0, 99)
                middle_name = female_middle_names[random_num]
            else:
                middle_name = None

            random_num = randint(0, 199)
            last_name = last_names[random_num]

            fake = Faker()

            end_date = date(year=2007, month=6, day=26)
            if treat_as:
                start_date = date(year=1970, month=1, day=1)
            else:
                start_date = "-80y"
            birthdate = fake.date_between(start_date, end_date)
            join_date = fake.date_between(start_date="-15y", end_date="now")

        # setting pronounce based on gender
        # and they way they treated
        if treat_as == 0:
            rand = randint(0, 1)
            pronounce = 0 if rand == 0 else 2
        elif gender == 0:
            pronounce = 0
        elif gender == 1:
            pronounce = 1
        else:
            rand = randint(0, 1)
            pronounce = 0 if rand == 0 else 1

        customers.append(
            {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "birthdate": birthdate,
                "gender": gender,
                "pronounce": pronounce,
                "join_date": join_date,
            }
        )

    return customers
