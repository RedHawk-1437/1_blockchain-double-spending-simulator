# config.py
# Central configuration for the simulator.

import os

# Proof-of-Work difficulty (leading zeros required)
DIFFICULTY = int(os.getenv("POW_DIFFICULTY", 3))

# Mining reward (float). Can be overridden with env var MINING_REWARD.
MINING_REWARD = float(os.getenv("MINING_REWARD", 10.0))

# Default currency used for mining rewards and default transactions.
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USDT")

# Network simulation latency bounds (seconds)
LATENCY_MIN = float(os.getenv("LATENCY_MIN", 0.0))
LATENCY_MAX = float(os.getenv("LATENCY_MAX", 5.0))

# Whether to validate transactions strictly (signatures). Not used here, placeholder.
STRICT_TX_VALIDATION = os.getenv("STRICT_TX_VALIDATION", "0") == "1"
