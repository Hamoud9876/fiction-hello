from random import randint
from core.data.data import address_type
from core.utils.generate_post_code import generate_post_code
from core.utils.random_string import random_string


def generate_address_data():
    """
    creates one recored for a customer with many changes
    -----------------------------------------
    args:  None
    -----------------------------------------
    return: a dict containing all available address
    for the customer
    """
    address = []
    # generate one address
    if randint(1, 5) > 1:
        address.append(
            {
                "first_line": random_string(randint(10, 20)),
                "second_line": random_string(randint(10, 20)),
                "city": random_string(randint(4, 20)),
                "county": random_string(randint(6, 30)),
                "post_code": generate_post_code(),
                "address_type": address_type[0],
            }
        )

    else:
        address.append(
            {
                "first_line": random_string(randint(10, 20)),
                "second_line": random_string(randint(10, 20)),
                "city": random_string(randint(4, 20)),
                "county": random_string(randint(6, 30)),
                "post_code": generate_post_code(),
                "address_type": address_type[0],
            }
        )
        address.append(
            {
                "first_line": random_string(randint(10, 20)),
                "second_line": random_string(randint(10, 20)),
                "city": random_string(randint(4, 20)),
                "county": random_string(randint(6, 30)),
                "post_code": generate_post_code(),
                "address_type": address_type[1],
            }
        )

    return address
