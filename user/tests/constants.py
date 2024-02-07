"""This module defines testconstants."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Payloads:
    VALID_PAYLOAD = {
        "email": "test@example.com",
        "password": "passwword123",
        "name": "Test name",
    }

    SHORT_PASSWORD_PAYLOAD = {
        "email": "test@example.com",
        "password": "pw",
        "name": "Test name",
    }

    CHARS_ONLY_PASSWORD_PAYLOAD = {
        "email": "test@example.com",
        "password": "passwordabc",
        "name": "Test name",
    }

    INTS_ONLY_PASSWORD_PAYLOAD = {
        "email": "test@example.com",
        "password": "123456789",
        "name": "Test name",
    }

    USER_DETAILS_PAYLOAD = {
        "name": "Test Name",
        "email": "test@example.com",
        "password": "test-user-password123",
    }
