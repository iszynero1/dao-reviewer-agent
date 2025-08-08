import os

# Agent Configuration
AGENT_CONTRACT = os.getenv("AGENT_CONTRACT", "ac.proxy.your_account.testnet") # Default to local dev
NETWORK_ID = os.getenv("NEAR_NETWORK", "testnet") # or "mainnet"

# DAO Configuration
WHITELIST = os.getenv("WHITELIST", "alice.near,bob.near").split(",")
BUDGET_LIMIT = int(os.getenv("BUDGET_LIMIT", "10000"))
APPROVAL_THRESHOLD = int(os.getenv("APPROVAL_THRESHOLD", "6"))
DEFAULT_SCORE = int(os.getenv("DEFAULT_SCORE", "8"))

# Scoring penalties
WHITELIST_PENALTY = int(os.getenv("WHITELIST_PENALTY", "3"))
BUDGET_PENALTY = int(os.getenv("BUDGET_PENALTY", "2"))

# Near RPC Configuration
NEAR_RPC_URL = os.getenv(
    "NEAR_RPC_URL",
    "https://rpc.testnet.near.org" if NETWORK_ID == "testnet" 
    else "https://rpc.mainnet.near.org"
)

# Phala Configuration (for TEE deployments)
PHALA_API_KEY = os.getenv("PHALA_API_KEY", "")