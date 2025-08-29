import unittest
from blockchain import Blockchain
from attack import AttackerNode


class TestBlockchain(unittest.TestCase):
    """
    Unit tests for Blockchain Simulator
    -----------------------------------
    Covers:
      - Transaction handling
      - Mining process
      - Attack simulation (51% attack)
      - Chain validation
      - Attack success metrics
      - Transaction history
    """

    def setUp(self):
        """Create a fresh blockchain and attacker before each test."""
        self.blockchain = Blockchain()
        self.attacker = AttackerNode(self.blockchain, hash_power=0.6)

    # --------------------------
    # TC01: Add Transaction
    # --------------------------
    def test_add_transaction(self):
        """Test that new transactions are added to pending pool."""
        tx = self.blockchain.add_transaction("Alice", "Bob", 50)
        self.assertIn(tx, self.blockchain.pending)

    # --------------------------
    # TC02: Mine Honest Block
    # --------------------------
    def test_mine_block(self):
        """Test that mining includes transactions and creates valid block."""
        self.blockchain.add_transaction("Alice", "Bob", 50)
        block = self.blockchain.mine_pending("Miner1")
        self.assertEqual(block.index, 1)  # Genesis block is 0, so mined block is 1
        self.assertTrue(block.hash.startswith("0" * self.blockchain.difficulty))  # Difficulty check

    # --------------------------
    # TC03: Execute 51% Attack
    # --------------------------
    def test_fifty_one_attack(self):
        """Test that attacker with >50% hash power can succeed in double-spend."""
        victim_tx = {"sender": "Alice", "receiver": "Merchant", "amount": 20, "currency": "USDT"}
        attacker_tx = {"sender": "Alice", "receiver": "Attacker", "amount": 20, "currency": "USDT"}

        success = self.attacker.fifty_one_attack(self.blockchain, victim_tx, attacker_tx)
        self.assertTrue(success)

    # --------------------------
    # TC04: Fork Resolution
    # --------------------------
    def test_chain_validity(self):
        """Test that blockchain remains valid after normal mining."""
        self.blockchain.add_transaction("Bob", "Charlie", 30)
        self.blockchain.mine_pending("Miner2")
        self.assertTrue(self.blockchain.is_chain_valid())

    # --------------------------
    # TC05: Attack Metrics Logging
    # --------------------------
    def test_attack_success_rate(self):
        """Test that attacker succeeds often with 60% hash power."""
        victim_tx = {"sender": "Alice", "receiver": "Merchant", "amount": 20, "currency": "USDT"}
        attacker_tx = {"sender": "Alice", "receiver": "Attacker", "amount": 20, "currency": "USDT"}

        successes = 0
        runs = 5
        for _ in range(runs):
            if self.attacker.fifty_one_attack(self.blockchain, victim_tx, attacker_tx):
                successes += 1

        success_rate = successes / runs
        self.assertGreater(success_rate, 0.5)

    # --------------------------
    # TC06: View Transaction History
    # --------------------------
    def test_transaction_history(self):
        """Test that mined block contains transaction history."""
        self.blockchain.add_transaction("Charlie", "Dave", 15)
        block = self.blockchain.mine_pending("Miner3")
        tx_list = block.transactions
        self.assertGreater(len(tx_list), 0)


if __name__ == "__main__":
    unittest.main()
