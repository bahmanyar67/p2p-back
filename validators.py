# validators.py
import re


class Validator:
    errors = {}
    error_messages = {
        "required": "This {field} is required.",
        "email": "Invalid email format.",
        "min": "This {field} must have at least {min_length} characters.",
        "max": "This {field} must have at most {max_length} characters.",
        "password": "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
        "string": "This {field} must contain only letters.",
        "number": "This {field} must be a number.",
        "boolean": "This {field} must be a boolean value.",
    }

    @staticmethod
    def validate(field, rules, data):
        value = data.get(field)
        Validator.errors = {}

        for rule in rules:
            if isinstance(rule, str):  # Simple rules like 'required'
                method = getattr(Validator, f"validate_{rule}", None)
                if method and not method(value):
                    Validator.add_error(field, Validator.error_messages[rule])
            elif isinstance(rule, list):  # Rules with parameters like ['min', 6]
                method = getattr(Validator, f"validate_{rule[0]}", None)
                if method and not method(value, *rule[1:]):
                    Validator.add_error(
                        field,
                        Validator.error_messages[rule[0]].format(
                            field=field, **{f"{rule[0]}_length": rule[1]}
                        )
                    )

        return not bool(Validator.errors)

    @staticmethod
    def validate_required(value):
        return value is not None and value != ""

    @staticmethod
    def validate_email(value):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", value))

    @staticmethod
    def validate_number(value):
        return str(value).isdigit() if value is not None else False

    @staticmethod
    def validate_boolean(value):
        return value in [0, 1, "0", "1", True, False]

    @staticmethod
    def validate_min(value, min_length):
        return len(value) >= min_length if value else False

    @staticmethod
    def validate_price(value):
        try:
            return float(value) >= 0  # Ensure the price is non-negative
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_string(value):
        return bool(re.match(r"^[A-Za-z\s]+$", value)) if value else False

    @staticmethod
    def validate_max(value, max_length):
        return len(value) <= max_length if value else False

    @staticmethod
    def validate_password(value):
        if not value:
            return False
        return (
                bool(re.search(r"[A-Z]", value)) and
                bool(re.search(r"[a-z]", value)) and
                bool(re.search(r"\d", value)) and
                bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", value))
        )

    @staticmethod
    def add_error(field, message):
        if field not in Validator.errors:
            Validator.errors[field] = []
        Validator.errors[field].append(message.format(field=field))

    @staticmethod
    def get_first_error(field):
        return Validator.errors.get(field, [None])[0] if field in Validator.errors else None

    @staticmethod
    def get_errors():
        return Validator.errors
