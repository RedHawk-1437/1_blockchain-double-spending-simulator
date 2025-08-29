# config.py
# Central configuration for the simulator.
# Instead of hardcoding values inside blockchain.py or app.py,
# we keep them here for easy modification and clarity.

import os

# Blockchain mining difficulty (number of leading zeros in proof-of-work).
# Higher value = harder mining, slower block confirmation.
DIFFICULTY = int(os.getenv("POW_DIFFICULTY", 3))

# Mining reward for successfully mining a block.
# Incentivizes miners and prevents network collapse.
MINING_REWARD = float(os.getenv("MINING_REWARD", 15.0))

# Default currency used for mining rewards and default transactions.
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USDT")