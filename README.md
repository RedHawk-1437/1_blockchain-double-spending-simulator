# 🪙 Blockchain Double Spending Simulator

A **Flask-based blockchain simulator** built in Python to demonstrate how double-spending attacks work in blockchain systems.  
The project simulates transactions, mining, and attacks like **Race Attack** and **51% Attack** in an educational, interactive way.

---

## 🚀 Features
- 🔗 **Blockchain Simulation** — create blocks, add transactions, and mine them.
- 💰 **Mining Rewards** — configurable reward system with difficulty settings.
- 🧑‍💻 **Transaction Handling** — send tokens between participants.
- ⚡ **Race Attack Simulation** — demonstrates invalidating a victim’s transaction with a conflicting one.
- 🏴 **51% Attack Simulation** — attacker with majority hash power can replace the honest chain.
- 🌐 **Web-based UI** — powered by Flask templates for easy interaction.

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **Flask** (for the web interface)
- **Custom Blockchain Engine** (`blockchain.py`)
- **Attack Module** (`attack.py`)
- **Config Module** (`config.py`)

---

## 📂 Project Structure

blockchain-double-spending-simulator/

│── app.py # Flask app (entry point)

│── blockchain.py # Blockchain logic

│── attack.py # AttackerNode logic (Race & 51% attack)

│── config.py # Default config (difficulty, rewards, etc.)

│── templates/ # HTML templates for UI

│── static/ # CSS, JS, images

│── requirements.txt # Python dependencies

│── README.md # Documentation (this file)

│── .gitignore

👨‍💻 Author

Developed by Eng.Muhammad Imtiaz Shaffi
BSCS Student | Aspiring Cybersecurity Professional