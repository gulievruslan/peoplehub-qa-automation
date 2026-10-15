"""Module contains enums"""
from enum import StrEnum


class NegativeAuth(StrEnum):
    """Negative auth enum"""
    NOT_VALID_EMAIL_ADDRESS = 'value is not a valid email address: An email address must have an @-sign.'
    VALID_STRING_INPUT = 'Input should be a valid string'
    INVALID_OR_EXPIRED_TOKEN = 'Invalid or expired token'
    NOT_AUTHENTICATED = 'Not authenticated'


class AppStatuses(StrEnum):
    """App statuses enum"""
    OK ='ok'


class LeaveRequestStatuses(StrEnum):
    """Leave request statuses enum"""
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class PayrollStatuses(StrEnum):
    """Payroll statuses enum"""
    PENDING = 'pending'