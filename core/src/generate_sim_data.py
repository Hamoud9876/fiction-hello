import string
import secrets


def generate_sims_data(value: int):
    """
    creates sims for each customer
    -----------------------------------------
    args: "value" represent the number of sims to be created

    -----------------------------------------
    return: list of all the sims
    """

    if not isinstance(value, int) or value == 0:
        return "Invalid value input"

    sims = []
    digits = string.digits
    for _ in range(value):
        sims.append(int("".join(secrets.choice(digits) for _ in range(9))))

    return sims
