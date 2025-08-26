# blockchain.py
"""
Blockchain core with currency-aware transactions and configurable mining reward.

Each transaction is a dictionary:
{
  "sender": "Alice",
  "receiver": "Bob",
  "amount": 12.5,
  "currency": "BTC"
}
"""

from __future__ import annotations
import hashlib
import json
import time
from dataclasses import dataclass
from typing import List, Dict, Any
from config import DIFFICULTY, MINING_REWARD, DEFAULT_CURRENCY


def sha256(data: str) -> str:
    """Return SHA-256 hex digest for the given string."""
    return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class Block:
    index: int
    previous_hash: str
    timestamp: float
    transactions: List[Dict[str, Any]]
    nonce: int = 0
    hash: str = ""

    def compute_hash(self) -> str:
        """
        Compute a deterministic hash of the block's content.
        Use json.dumps with sort_keys so serialization is stable.
        """
        block_dict = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "nonce": self.nonce
        }
        return sha256(json.dumps(block_dict, sort_keys=True, default=str))


class Blockchain:
    def __init__(self, difficulty: int = DIFFICULTY,
                 reward_amount: float = MINING_REWARD,
                 reward_currency: str = DEFAULT_CURRENCY):
        """
        Create a new blockchain instance.

        - difficulty: PoW difficulty (number of leading zeros)
        - reward_amount: mining reward amount
        - reward_currency: currency code for mining rewards (e.g. USDT)
        """
        self.difficulty = difficulty
        self.reward_amount = float(reward_amount)
        self.reward_currency = reward_currency
        self.chain: List[Block] = []
        self.pending: List[Dict[str, Any]] = []  # mempool of tx dicts
        self.create_genesis()

    def create_genesis(self) -> None:
        """Create the genesis block and append to chain."""
        genesis_tx = {
            "sender": "Network",
            "receiver": "genesis",
            "amount": 0.0,
            "currency": self.reward_currency
        }
        genesis = Block(index=0, previous_hash="0"*64, timestamp=time.time(),
                        transactions=[genesis_tx], nonce=0)
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, sender: str, receiver: str, amount: float, currency: str = None) -> Dict[str, Any]:
        """
        Add a transaction to the pending pool.

        :param sender: sender id (string)
        :param receiver: receiver id (string)
        :param amount: numeric amount (>0)
        :param currency: currency code string (e.g. 'USDT', 'BTC')
        :return: the transaction dict appended
        :raises: ValueError on invalid amount
        """
        if currency is None:
            currency = self.reward_currency

        try:
            amt = float(amount)
        except Exception:
            raise ValueError("Amount must be numeric")

        if amt <= 0:
            raise ValueError("Amount must be greater than zero")

        tx = {
            "sender": sender,
            "receiver": receiver,
            "amount": amt,
            "currency": currency
        }
        self.pending.append(tx)
        return tx

    def proof_of_work(self, block: Block) -> str:
        """Simple PoW: find nonce so that hash starts with difficulty zeros."""
        block.nonce = 0
        computed = block.compute_hash()
        target = "0" * self.difficulty
        while not computed.startswith(target):
            block.nonce += 1
            computed = block.compute_hash()
        return computed

    def mine_pending(self, miner_address: str) -> Block:
        """
        Mine a new block including all pending transactions plus the mining reward.
        After mining, pending pool is cleared.
        """
        # Copy pending txs to include in block
        txs = list(self.pending)

        # Append reward transaction (coinbase)
        reward_tx = {
            "sender": "Network",
            "receiver": miner_address,
            "amount": float(self.reward_amount),
            "currency": self.reward_currency
        }
        txs.append(reward_tx)

        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_last_block().hash,
            timestamp=time.time(),
            transactions=txs
        )

        # Mine
        new_block.hash = self.proof_of_work(new_block)

        # Append to chain and clear pending mempool
        self.chain.append(new_block)
        self.pending = []
        return new_block

    def is_chain_valid(self) -> bool:
        """Validate chain integrity (hashes and links)."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.hash:
                return False
            if current.compute_hash() != current.hash:
                return False
        return True

    # Utility: convert block objects to serializable dicts (for templates / API)
    def to_serializable_chain(self) -> List[Dict[str, Any]]:
        result = []
        for b in self.chain:
            result.append({
                "index": b.index,
                "previous_hash": b.previous_hash,
                "timestamp": b.timestamp,
                "nonce": b.nonce,
                "hash": b.hash,
                "transactions": b.transactions
            })
        return result
