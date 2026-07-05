"""Authentication helpers."""

import hashlib
import re

from backend import database as db


def hash_password(password):
    """Hash a password with SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password, password_hash):
    """Check if password matches hash."""
    return hash_password(password) == password_hash


def validate_email(email):
    """Basic email format check."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_username(username):
    """Username must be 3-20 alphanumeric/underscore characters."""
    return bool(re.match(r"^[a-zA-Z0-9_]{3,20}$", username))


def register_user(username, email, password, full_name=""):
    """Register a new user. Returns (success, message)."""
    if not validate_username(username):
        return False, "Username must be 3-20 characters (letters, numbers, underscore)."
    if not validate_email(email):
        return False, "Please enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    password_hash = hash_password(password)
    user_id = db.create_user(username, email, password_hash, full_name)
    if user_id is None:
        return False, "Username or email already exists."
    return True, "Account created successfully!"


def login_user(username, password):
    """Authenticate user. Returns (success, user_or_message)."""
    user = db.get_user_by_username(username)
    if not user:
        return False, "Invalid username or password."
    if not verify_password(password, user["password_hash"]):
        return False, "Invalid username or password."
    return True, user
