from enum import Enum, auto
class ResponseType(Enum):
    LOGIN = auto()
    LOGOUT = auto()
    TOKENEXPIRE = auto()
    REFRESH = auto()

    CUSTOMERS = auto()
    JOBS = auto()
    TASKS = auto()

    ERROR = auto()
    ACCOUNTERROR = auto()