# attack.py
"""
Attack simulation module for blockchain.
Implements:
 - Race Attack
 - 51% Attack (majority attack)
"""

import time
import random
from blockchain import Blockchain, Block


class AttackerNode:
    def __init__(self, blockchain: Blockchain, hash_power: float = 0.6):
        """
        Initialize attacker node.

        :param blockchain: Blockchain instance (shared with honest network).
        :param hash_power: fraction of total mining power attacker controls (0-1).
                           Example: 0.6 means attacker has 60% hash power.
        """
        self.blockchain = blockchain
        self.hash_power = hash_power

    # ------------------------------------------------------------
    # Race Attack
    # ------------------------------------------------------------
    def race_attack(self, blockchain: Blockchain, victim_tx: dict, attacker_tx: dict) -> bool:
        """
        Perform a Race Attack.

        Idea:
        - Victim receives a TX (sender → victim).
        - Attacker quickly tries to broadcast a conflicting TX (sender → attacker).
        - If attacker’s TX confirms in a block before victim’s TX, attack succeeds.
        - If honest miners confirm victim’s TX first, attack fails.

        :param blockchain: Blockchain instance
        :param victim_tx: transaction dict (sender → victim)
        :param attacker_tx: transaction dict (sender → attacker)
        :return: True if attack succeeds, False otherwise
        """
        print("\n🚨 Starting Race Attack...")

        # Honest miner includes victim’s transaction
        blockchain.pending.append(victim_tx)
        honest_block = blockchain.mine_pending("HonestMiner")
        print(f"✅ Victim sees transaction included in Block {honest_block.index}")

        # Attacker attempts to mine a conflicting transaction
        attacker_chain = Blockchain(difficulty=blockchain.difficulty,
                                    reward_amount=blockchain.reward_amount,
                                    reward_currency=blockchain.reward_currency)
        attacker_chain.chain = list(blockchain.chain)  # copy honest chain up to this point
        attacker_chain.pending.append(attacker_tx)

        fake_block = attacker_chain.mine_pending("Attacker")
        print(f"🕵️ Attacker mines fake Block {fake_block.index} with double-spend TX")

        # Decide which chain wins:
        # If attacker had >50% hash power, they have better chance to win.
        if self.hash_power > 0.5 and random.random() < self.hash_power:
            blockchain.chain = attacker_chain.chain
            print("💀 Race Attack SUCCESS — attacker’s TX replaced victim’s TX")
            return True
        else:
            print("✅ Race Attack FAILED — honest chain longer")
            return False

    # ------------------------------------------------------------
    # 51% Attack
    # ------------------------------------------------------------
    def fifty_one_attack(self, blockchain: Blockchain, victim_tx: dict, attacker_tx: dict) -> bool:
        """
        Perform a 51% attack (majority attack).

        Idea:
        - Attacker privately mines a secret chain containing attacker’s TX.
        - Honest chain grows with victim’s TX.
        - If attacker can outpace honest miners (due to majority hash power),
          they reveal their longer chain, invalidating victim’s TX.

        :param blockchain: Blockchain instance
        :param victim_tx: transaction dict (sender → victim)
        :param attacker_tx: transaction dict (sender → attacker)
        :return: True if attack succeeds, False otherwise
        """
        print("\n🚨 Starting 51% Attack...")

        # Honest miners confirm victim’s TX
        blockchain.pending.append(victim_tx)
        victim_block = blockchain.mine_pending("HonestMiner")
        print(f"✅ Victim sees transaction confirmed in Block {victim_block.index}")

        # Attacker secretly starts a private fork
        attacker_chain = Blockchain(difficulty=blockchain.difficulty,
                                    reward_amount=blockchain.reward_amount,
                                    reward_currency=blockchain.reward_currency)
        attacker_chain.chain = list(blockchain.chain[:-1])  # fork before victim block
        attacker_chain.pending.append(attacker_tx)

        private_block = attacker_chain.mine_pending("Attacker")
        print(f"🕵️ Attacker mines private Block {private_block.index}")

        # Attacker keeps mining additional private blocks
        while len(attacker_chain.chain) <= len(blockchain.chain):
            attacker_chain.pending.append({
                "sender": "Network",
                "receiver": "Attacker",
                "amount": 0,
                "currency": blockchain.reward_currency
            })
            private_block = attacker_chain.mine_pending("Attacker")
            print(f"🕵️ Attacker mines private Block {private_block.index}")
            time.sleep(0.5)  # simulate time delay

        # Replace honest chain if attacker’s is longer
        if len(attacker_chain.chain) > len(blockchain.chain):
            blockchain.chain = attacker_chain.chain
            print("💀 51% Attack SUCCESS — attacker’s chain replaces honest chain!")
            return True
        else:
            print("✅ 51% Attack FAILED — honest chain stayed longer")
            return False