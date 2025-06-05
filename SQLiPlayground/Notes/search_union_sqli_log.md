
# SQL Injection Test Log – UNION-based Extraction on `/search`

**Timestamp:** 2025-06-04 01:02:28  
**Test Type:** UNION-based SQL Injection  
**HTTP Method:** GET  
**Vulnerable Parameter:** `q`  
**Payload Used:** `' UNION SELECT username, password FROM users -- `

---

## 🔍 What Happened:

The payload appended a UNION-based SQL query to the existing search. Since the query returned a valid row set (`username, password`), the server displayed all users.

This confirms:
- Column count in the original query is **2**
- UNION injection is **successful**
- No filtering or WAF blocking this injection

---

## 🔒 Exploitability:

This vulnerability allows:
- **Credential harvesting** (all users and passwords)
- **User impersonation**
- **Full data disclosure**

---

## 🧠 Next Steps for Exploitation:

- Automate data harvesting
- Try to inject more columns
- Test with `information_schema.tables` or `columns` for database fingerprinting

