import secrets
import string

def random_string(str_length: int):
    """
    generates a random string with predetermined length
    -----------------------------------------
    args:  str_length: int determins the length
    of the produced string
    -----------------------------------------
    return: string with the provided length
    """
    if not isinstance(str_length, int):
        return "Not a valid length"
    alphabet = string.ascii_letters 
    rand_str = (''.join(secrets.choice(alphabet) 
                          for _ in range(str_length)))
    
    return rand_str