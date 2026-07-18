import re
from getpass import getpass
import requests

POINTS_PER_CHECK = 5
MIN_PASSWORD_LENGTH = 8

def matches(pattern:str,text:str) -> bool:
    return bool(re.search(pattern,text))

def search_lowercase(password:str) -> bool:
    """Return True if the text contains at least one lowercase letter."""
    return matches(r"[a-z]", password)


def search_uppercase(password:str) -> bool:
    """Return True if the text contains at least one uppercase letter."""
    return matches(r"[A-Z]", password)


def search_digits(password:str) -> bool:
    """Return True if the text contains at least one digit."""
    return matches(r"\d", password)


def search_special_characters(password:str) -> bool:
    """Return True if the text contains at least one special character."""
    return matches(r"[^a-zA-Z0-9]", password)


def fetch_weak_passwords() -> list:
    """Fetch a list of common weak passwords from GitHub."""
    try:
        req = requests.get(
            "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt",
            timeout=5,
        )
        req.raise_for_status()
        return req.text.splitlines()
    except requests.RequestException:
        return []

def check_repeated_chars(password:str) -> bool:
    seen = set()
    for char in password:
        if char in seen:
            return True
        seen.add(char)
        
    return False


def main():
    """Run the password strength checker."""
    password = getpass("Enter Password : ")

    if not password:
        print("Password cannot be empty")
        return

    weak_passwords = fetch_weak_passwords()

    repeated_chars = check_repeated_chars(password)

    if repeated_chars:
        print("Password contains duplicate characters.")
        return

    if weak_passwords and password in weak_passwords:
        print("Your password is very weak!")
        return

    score = 0
    strength = "Weak"

    if len(password) >= MIN_PASSWORD_LENGTH:
        score += POINTS_PER_CHECK

        checks = {
            "Digits": search_digits,
            "Lowercase": search_lowercase,
            "Uppercase": search_uppercase,
            "Special Characters": search_special_characters,
        }

        for key, check in checks.items():
            if check(password):
                score += POINTS_PER_CHECK
                print(f"{key} ✅")
            else:
                print(f"{key} ❌")

        print(f"Length : {len(password)} ✅")

        if score < 10 and score > 0:
            strength = "Weak"
        elif score >= 11 and score <= 15:
            strength = "Medium"
        elif score >= 20 and score <= 25:
            strength = "Strong"
        else:
            print("Error!")

        print(f"Strength: {strength}")
        print(f"Score : {score} / 25")
    else:
        print("🔔 Password must be at least 8 characters long")


main()