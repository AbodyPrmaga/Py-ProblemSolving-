import re
from getpass import getpass
import requests
    
def search_lowercase(text):
    return bool(re.search(r"[a-z]",text))

def search_uppercase(text):
    return bool(re.search(r"[A-Z]",text))
    
def search_digits(text):
    return bool(re.search(r"\d",text))

def search_special_characters(text):

    return bool(re.search(r"[^a-zA-Z0-9]",text))

def request_weakpass():
    try:
        req = requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt")
        return req.text.splitlines()
    except requests.RequestException:
        return

def main():

    password = getpass("Enter Password : ")
    if not password : 
        print("Password cannot be empty")
        return
    weak_passwords = request_weakpass()
    if weak_passwords and password in weak_passwords:
        print("Your password is very weak!")
        return

    score = 0
    strength = "Weak"

    if len(password) >= 8:

        checks = {
            "Digits": search_digits,
            "Lowercase": search_lowercase,
            "Uppercase": search_uppercase,
            "Special Characters": search_special_characters
        }

        for key,check in checks.items():
            if check(password):
                score += 5
                print(f"{key}  ✅")
            else:
                print(f"{key} ❌")

        print(f"Length : {len(password)} ✅")

        if score <= 10 :
            strength = "Weak"
        elif score <= 15 :
            strength = "Medium"
        else:
            strength = "Strong"

        print(f"Strength: {strength}")

        print(f"Score :  {score} / 20")

    else:
        print("🔔 Password must be at least 8 characters long")

main()