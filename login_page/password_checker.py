import re

def password_validator(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit."
    special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
    if not re.search(special_characters, password):
        return False, "Password must contain at least one special character."
    return True, "Password is valid."

