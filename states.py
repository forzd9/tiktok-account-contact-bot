# states.py
# تعريف حالات المحادثة المختلفة

from enum import IntEnum, auto

class States(IntEnum):
    """حالات المحادثة لجميع العمليات"""
    SELECTING_ACTION = auto()

    # ربط رقم
    BIND_NUMBER_SESSION = auto()
    BIND_NUMBER_MOBILE = auto()
    BIND_NUMBER_CODE = auto()

    # ربط بريد
    BIND_EMAIL_SESSION = auto()
    BIND_EMAIL_ADDRESS = auto()
    BIND_EMAIL_CODE = auto()

    # فك رقم
    UNBIND_NUMBER_SESSION = auto()
    UNBIND_NUMBER_CONFIRM = auto()
    UNBIND_NUMBER_TICKET = auto()

    # فك بريد
    UNBIND_EMAIL_SESSION = auto()
    UNBIND_EMAIL_CONFIRM = auto()
    UNBIND_EMAIL_TICKET = auto()

    # ربط رقم + فك بريد
    BIND_NUMBER_UNBIND_EMAIL_SESSION = auto()
    BIND_NUMBER_UNBIND_EMAIL_MOBILE = auto()
    BIND_NUMBER_UNBIND_EMAIL_CODE = auto()
    BIND_NUMBER_UNBIND_EMAIL_VERIFY = auto()
    BIND_NUMBER_UNBIND_EMAIL_TICKET = auto()

    # ربط بريد + فك رقم
    BIND_EMAIL_UNBIND_NUMBER_SESSION = auto()
    BIND_EMAIL_UNBIND_NUMBER_EMAIL = auto()
    BIND_EMAIL_UNBIND_NUMBER_CODE = auto()
    BIND_EMAIL_UNBIND_NUMBER_VERIFY = auto()
    BIND_EMAIL_UNBIND_NUMBER_TICKET = auto()