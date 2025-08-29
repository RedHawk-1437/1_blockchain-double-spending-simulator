# 🪙 Blockchain Double Spending Attack Simulator

A blockchain simulator built with **Python + Flask** that demonstrates how double-spending attacks (such as 51% Attack and Race Attack) can compromise blockchain integrity.

---

## 🚀 Features
- ✅ Core Blockchain implementation with:
  - Proof-of-Work (configurable difficulty)
  - Mining rewards in multiple currencies (default: USDT)
  - Transaction handling (sender, receiver, amount, currency)
- ✅ Web-based interface (Flask + HTML + Bootstrap)
- ✅ Simulation of **double spending attacks**:
  - **51% Attack** (attacker controls majority hash power)
  - **Race Attack** (attacker tries to reverse a transaction quickly)
- ✅ Peer-to-Peer node communication:
  - Broadcasting blocks and transactions
  - Simple consensus (longest chain rule)
- ✅ Unit tests to validate blockchain integrity and attack scenarios

---

## 📂 Project Structure
blockchain_double_spending_simulator/

│── app.py # Flask web app (UI + routes)

│── blockchain.py # Core blockchain logic (PoW, transactions, mining)

│── attack.py # Attacker simulation (Race attack, 51% attack)

│── node.py # Node implementation (peers, sync, broadcast)

│── config.py # Global configuration (difficulty, rewards, currency)

│── requirements.txt # Python dependencies

│── README.md # Project documentation

│── test/
│ └── test_blockchain.py # Unit tests for blockchain & attacks

│── templates/
│ ├── index.html # Homepage (attack options)
│ ├── attack_result.html # Attack result display

│── static/
│ ├── vu_logo.png # University logo
│ └── my_photo.jpg # Developer photo

└── .gitignore # Ignore venv, cache, etc


---

## ⚙️ Installation & Setup
### 1. Clone Repository
```bash
git clone https://github.com/your-username/1_blockchain_double_spending_simulator.git
cd 1_blockchain_double_spending_simulator

2. Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate   # (Linux/Mac)
.venv\Scripts\activate      # (Windows)

3. Install Dependencies
pip install -r requirements.txt

4. Run Flask App
python app.py
Open browser → http://127.0.0.1:5000/

🧪 Running Tests
Run all blockchain tests:
python -m unittest test/test_blockchain.py

Expected output ✅:
Ran 6 tests in 4.0s
OK

👨‍💻 Author

Eng.Muhammad Imtiaz Shaffi
BC220200917
BSCS Final Year Project, Virtual University