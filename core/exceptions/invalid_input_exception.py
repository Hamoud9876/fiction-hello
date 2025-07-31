import inspect


class InvalidInput(Exception):
    def __init__(self, message=None):
        caller_frame = inspect.currentframe().f_back
        func_name = caller_frame.f_code.co_name

        default_message = f"Invalid input in function '{func_name}'"
        full_message = message or default_message

        super().__init__(full_message)
