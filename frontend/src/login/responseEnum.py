from enum import Enum, auto
class ResponseType(Enum):
    LOGIN = auto()
    LOGOUT = auto()
    TOKENEXPIRE = auto()
    REFRESH = auto()

    ADDCUSTOMERS = auto()
    GETCUSTOMERS = auto()

    ADDJOBS = auto()
    GETJOBS = auto()
    
    SETTASKS = auto()
    GETTASKS = auto()

    ERROR = auto()
    ACCOUNTERROR = auto()