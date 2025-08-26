# app.py
"""
Flask GUI + routing for the blockchain simulator.
This version expects:
 - blockchain.Blockchain (blockchain.py)
 - attack.AttackerNode (attack.py) - existing in your project
"""

from flask import Flask, render_template, request
from blockchain import Blockchain
from attack import AttackerNode
from config import DEFAULT_CURRENCY, MINING_REWARD, DIFFICULTY

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Instantiate blockchain and attacker
blockchain = Blockchain(difficulty=DIFFICULTY,
                        reward_amount=MINING_REWARD,
                        reward_currency=DEFAULT_CURRENCY)

# AttackerNode uses the blockchain instance (attack.py should accept this)
attacker = AttackerNode(blockchain, hash_power=0.6)


def render_home(message: str = None, status: str = None):
    """
    Helper that renders index.html with required template variables.
    - chain is list of serializable block dicts
    - blockchain passed to access pending mempool etc.
    - popup_message/status used by modal
    """
    chain_data = blockchain.to_serializable_chain()
    return render_template("index.html",
                           chain=chain_data,
                           blockchain=blockchain,
                           popup_message=message,
                           popup_status=status)


@app.route("/", methods=["GET"])
def index():
    return render_home()


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    try:
        sender = request.form["sender"]
        receiver = request.form["receiver"]
        amount = request.form["amount"]
        currency = request.form.get("currency") or blockchain.reward_currency
        tx = blockchain.add_transaction(sender, receiver, amount, currency=currency)
        msg = f"✅ Transaction added: {tx['amount']} {tx['currency']} — {tx['sender']} → {tx['receiver']}"
        return render_home(msg, "success")
    except Exception as e:
        return render_home(f"❌ Failed to add transaction: {e}", "error")


@app.route("/mine", methods=["GET"])
def mine():
    try:
        miner_id = "WebMiner"
        block = blockchain.mine_pending(miner_id)
        # reward is last tx in block.transactions
        reward = block.transactions[-1]
        msg = f"✅ Block {block.index} mined. Reward: {reward['amount']} {reward['currency']} to {reward['receiver']}"
        return render_home(msg, "success")
    except Exception as e:
        return render_home(f"❌ Mining failed: {e}", "error")


@app.route("/race_attack", methods=["POST"])
def race_attack():
    try:
        amount = float(request.form["amount"])
        victim_tx = {
            "sender": request.form["sender"],
            "receiver": request.form["victim"],
            "amount": amount,
            "currency": request.form.get("currency") or blockchain.reward_currency
        }
        attacker_tx = {
            "sender": request.form["sender"],
            "receiver": request.form["attacker"],
            "amount": amount,
            "currency": victim_tx["currency"]
        }

        success = attacker.race_attack(blockchain, victim_tx, attacker_tx)
        if success:
            return render_home("💀 Race Attack SUCCESS — victim's transaction was invalidated!", "success")
        else:
            return render_home("✅ Race Attack FAILED — blockchain resisted the attack.", "error")
    except Exception as e:
        return render_home(f"❌ Race attack error: {e}", "error")


@app.route("/fifty_one_attack", methods=["POST"])
def fifty_one_attack():
    try:
        amount = float(request.form["amount"])
        victim_tx = {
            "sender": request.form["sender"],
            "receiver": request.form["victim"],
            "amount": amount,
            "currency": request.form.get("currency") or blockchain.reward_currency
        }
        attacker_tx = {
            "sender": request.form["sender"],
            "receiver": request.form["attacker"],
            "amount": amount,
            "currency": victim_tx["currency"]
        }

        success = attacker.fifty_one_attack(blockchain, victim_tx, attacker_tx)
        if success:
            return render_home("💀 51% Attack SUCCESS — attacker's chain replaced the honest chain!", "success")
        else:
            return render_home("✅ 51% Attack FAILED — honest chain remained secure.", "error")
    except Exception as e:
        return render_home(f"❌ 51% attack error: {e}", "error")


# Prevent aggressive caching while developing
@app.after_request
def add_header(resp):
    resp.headers["Cache-Control"] = "no-store"
    return resp


if __name__ == "__main__":
    # Run debug server for development
    app.run(host="0.0.0.0", port=5000, debug=True)
