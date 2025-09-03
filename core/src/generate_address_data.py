from random import randint, choice
from core.data.data import address_type
from faker import Faker


fake = Faker("en_GB")


def generate_address_data():
    """
    creates one recored for a customer with many changes
    -----------------------------------------
    args:  None
    -----------------------------------------
    return: a dict containing all available address
    for the customer
    """

    #a list of counties as faker does not support uk counties
    COUNTIES = [
    "Greater London", "West Midlands", "Greater Manchester", "Merseyside",
    "South Yorkshire", "West Yorkshire", "Tyne and Wear", "Hampshire",
    "Kent", "Essex", "Surrey", "Lancashire", "Devon", "Cornwall"
]
    address = []
    # 80% chance to generate one address
    if randint(1, 5) > 1:
        address.append(
            {
                "first_line": fake.street_address(),
                "second_line": fake.secondary_address() if randint(1,5) > 1 else "",
                "city": fake.city(),
                "county": choice(COUNTIES),
                "post_code": fake.postcode(),
                "address_type": address_type[0],
            }
        )

    else:
        #20% chance to generate 2 address type home and work
        address.append(
            {
                "first_line": fake.street_address(),
                "second_line": fake.secondary_address() if randint(1,5) > 1 else "",
                "city": fake.city(),
                "county": choice(COUNTIES),
                "post_code": fake.postcode(),
                "address_type": address_type[0],
            }
        )
        address.append(
            {
                "first_line": fake.street_address(),
                "second_line": fake.secondary_address() if randint(1,5) > 1 else "",
                "city": fake.city(),
                "county": choice(COUNTIES),
                "post_code": fake.postcode(),
                "address_type": address_type[0],
            }
        )

    return address
