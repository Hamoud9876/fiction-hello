import inspect
import logging


logging.basicConfig(
    filename="app_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class InvalidInput(Exception):
    def __init__(self, message=None):
        caller_frame = inspect.currentframe().f_back
        func_name = caller_frame.f_code.co_name

        default_message = f"Invalid input in function '{func_name}'"
        full_message = message or default_message

        logging.error(full_message)
        super().__init__(full_message)
