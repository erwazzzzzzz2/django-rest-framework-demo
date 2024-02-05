class Payloads:
    @staticmethod
    def success_payload():
        return {
            "email": "test@example.com",
            "password": "passwword123",
            "name": "Test name",
        }

    @staticmethod
    def email_short_payload():
        return {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test name",
        }

    @staticmethod
    def pwd_chars_only_payload():
        return {
            "email": "test@example.com",
            "password": "passwordabc",
            "name": "Test name",
        }

    @staticmethod
    def pwd_ints_only_payload():
        return {
            "email": "test@example.com",
            "password": "123456789",
            "name": "Test name",
        }
