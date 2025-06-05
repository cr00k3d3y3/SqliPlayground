# SqliPlayground
# 🧠 SqliPlayground

A deliberately vulnerable web application built for learning and practicing SQL Injection (SQLi) techniques in a safe, controlled environment.

---

## 🚀 Features

- 💥 Multiple SQLi Scenarios: Error-based, Boolean-based, Blind, Union-based, etc.
- 🎯 Difficulty Levels: Beginner to Advanced
- 🔐 Secure vs Insecure Examples
- 🧪 CTF-style challenges and flags
- 🧰 Integration-ready with tools like SQLMap and Burp Suite
- 📝 Step-by-step tutorials for each vulnerability

---

## 📚 Learning Objectives

By using this playground, you will:

- Understand how different types of SQL Injections work
- Learn to exploit and identify SQL vulnerabilities in real-world-like applications
- Practice writing payloads and using automation tools
- Compare insecure code with secure coding practices

---

## ⚙️ Installation

**Requirements:**

- Python 3.8+
- pip
- Git

```bash
# Clone the repository
git clone https://github.com/cr00k3d3y3/SqliPlayground.git
cd SqliPlayground

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
