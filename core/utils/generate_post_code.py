from random import randint
import string
import secrets


def generate_post_code():
    """
    generate a random post code
    -----------------------------------------
    args:  None
    -----------------------------------------
    return: string representing a post code
    """

    alphabet = string.ascii_letters
    post_code = "".join(
        secrets.choice(alphabet) if i in [0, 4, 3] else str(randint(1, 20))
        for i in range(4)
    )
    post_code = post_code.upper()

    return post_code
