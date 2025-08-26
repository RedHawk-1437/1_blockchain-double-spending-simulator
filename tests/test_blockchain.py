import unittest
from blockchain import Blockchain, Block
from attack import AttackerNode


class TestBlockchain(unittest.TestCase):

    def setUp(self):
        """Create a fresh blockchain before each test"""
        self.blockchain = Blockchain()
        self.attacker = AttackerNode(self.blockchain, hash_power=0.6)

    # --------------------------
    # TC01: Add Transaction
    # --------------------------
    def test_add_transaction(self):
        tx = self.blockchain.add_transaction("Alice", "Bob", 50)
        self.assertIn(tx, self.blockchain.pending_transactions)

    # --------------------------
    # TC02: Mine Honest Block
    # --------------------------
    def test_mine_block(self):
        self.blockchain.add_transaction("Alice", "Bob", 50)
        block = self.blockchain.mine_pending_transactions("Miner1")
        self.assertEqual(block.index, 1)  # Genesis block = 0, so next is 1
        self.assertTrue(block.hash.startswith("00"))  # Difficulty check

    # --------------------------
    # TC03: Execute 51% Attack
    # --------------------------
    def test_fifty_one_attack(self):
        victim_tx = {"sender": "Alice", "receiver": "Merchant", "amount": 20}
        attacker_tx = {"sender": "Alice", "receiver": "Attacker", "amount": 20}

        success = self.attacker.fifty_one_attack(self.blockchain, victim_tx, attacker_tx)
        self.assertTrue(success)  # With 60% hash power, attacker usually wins

    # --------------------------
    # TC04: Fork Resolution
    # --------------------------
    def test_chain_validity(self):
        # Mine a valid block
        self.blockchain.add_transaction("Bob", "Charlie", 30)
        self.blockchain.mine_pending_transactions("Miner2")
        # Blockchain should remain valid
        self.assertTrue(self.blockchain.is_chain_valid())

    # --------------------------
    # TC05: Attack Metrics Logging
    # --------------------------
    def test_attack_success_rate(self):
        victim_tx = {"sender": "Alice", "receiver": "Merchant", "amount": 20}
        attacker_tx = {"sender": "Alice", "receiver": "Attacker", "amount": 20}

        successes = 0
        runs = 5
        for _ in range(runs):
            if self.attacker.fifty_one_attack(self.blockchain, victim_tx, attacker_tx):
                successes += 1

        success_rate = successes / runs
        self.assertGreater(success_rate, 0.5)  # Attacker should succeed often

    # --------------------------
    # TC06: View Transaction History
    # --------------------------
    def test_transaction_history(self):
        self.blockchain.add_transaction("Charlie", "Dave", 15)
        block = self.blockchain.mine_pending_transactions("Miner3")
        tx_list = block.transactions
        self.assertGreater(len(tx_list), 0)


if __name__ == "__main__":
    unittest.main()
