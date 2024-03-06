import logging
from inputimeout import inputimeout, TimeoutOccurred

class Debugging:
    """
    Handles all debugging levels and logging.

    Constant values:
        Debugging.DEBUG_OFF: Defines that won't be logged messages.
        Debugging.DEBUG_MIN: Only the most important messages will be logged.
        Debugging.DEBUG_MAIN: Some messages for common errors will be logged.
        Debugging.DEBUG_MAX: All messages will be logged.
    """

    DEBUG_OFF = 0
    DEBUG_MIN = 1
    DEBUG_MAIN = 2
    DEBUG_MAX = 999

    __monostate = None

    def __init__(self, level=DEBUG_OFF, showBrowser=False):
        if not Debugging.__monostate:
            Debugging.__monostate = self.__dict__
            self.level = level
            self.showBrowser = showBrowser
        else:
            self.__dict__ = Debugging.__monostate


    def equal_or_greater_than(self, level):
        return (self.level >= level)

    def _print(self, message, type='info', minLevel=DEBUG_OFF, printDefaultHandler=False):
        if self.equal_or_greater_than(minLevel):
            if self.equal_or_greater_than(Debugging.DEBUG_MAX) or printDefaultHandler:
                print(message)
            if type == 'info':
                logging.info(message)
            elif type == 'error':
                logging.error(message)
            elif type == 'exception':
                logging.exception(message)

    def print_info(self, message, minLevel=DEBUG_MAIN, printDefaultHandler=False):
        self._print(message, 'info', minLevel, printDefaultHandler)

    def print_error(self, message, minLevel=DEBUG_OFF):
        self._print(message, 'error', minLevel)

    def print_exception(self, message, minLevel=DEBUG_OFF):
        self._print(message, 'exception', minLevel)

    def _user_input_or_default(self, message, max_wait, default=False):
        if max_wait:
            print(f"You have {max_wait} seconds to answer!")
            print(message)
            try:
                answer = inputimeout(prompt='>>', timeout=5)
                return answer == 'yes'
            except TimeoutOccurred:
                return default
            else:
                return default
        return default