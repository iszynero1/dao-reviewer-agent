import os
import json
import asyncio
from near_api.signer import KeyPair
from near_api.providers import JsonProvider
from near_api.account import Account
from typing import Dict, Any, Optional

class ShadeAgent:
    def __init__(
        self,
        contract_id: str,
        network: str = "testnet",
        key_derivation_path: str = "m/44'/397'/0'"
    ):
        self.contract_id = contract_id
        self.network = network
        self.key_derivation_path = key_derivation_path
        self.provider = JsonProvider(
            "https://rpc.testnet.near.org" if network == "testnet" 
            else "https://rpc.mainnet.near.org"
        )
        self.key_pair = self._load_key_pair()
        self.account = Account(self.provider, self.contract_id, self.key_pair)

    def _load_key_pair(self) -> KeyPair:
        """Load key pair from environment variable"""
        private_key = os.getenv("NEAR_PRIVATE_KEY")
        if not private_key:
            raise ValueError("NEAR_PRIVATE_KEY environment variable not set")
        return KeyPair.from_string(private_key)

    async def register(self) -> Dict[str, Any]:
        """Register the agent with the Shade protocol"""
        return await self.account.function_call(
            "register",
            {},
            gas=30000000000000,
            amount=0
        )

    async def get_account_id(self) -> str:
        """Get the agent's account ID"""
        return self.contract_id

    async def get_account_balance(self, account_id: Optional[str] = None) -> str:
        """Get account balance"""
        account_to_check = account_id or self.contract_id
        account = Account(self.provider, account_to_check)
        balance = await account.get_account_balance()
        return balance["available"]

    async def get_derived_account(self, chain: str) -> str:
        """Get derived account ID for another chain (like Ethereum)"""
        result = await self.account.view_function(
            self.contract_id,
            "get_derived_account",
            {"chain": chain}
        )
        return result["result"]

    async def submit_transaction(
        self,
        payload: Dict[str, Any],
        receiver_id: str,
        actions: list
    ) -> Dict[str, Any]:
        """Submit a transaction through the agent"""
        result = await self.account.function_call(
            receiver_id,
            "submit",
            {
                "payload": payload,
                "actions": actions
            },
            gas=30000000000000,
            amount=0
        )
        return result

    async def request_signature(
        self,
        payload: Dict[str, Any],
        derivation_path: str,
        key_version: str = "ed25519"
    ) -> Dict[str, Any]:
        """Request a signature from the agent"""
        result = await self.account.function_call(
            self.contract_id,
            "request_signature",
            {
                "payload": payload,
                "derivation_path": derivation_path,
                "key_version": key_version
            },
            gas=30000000000000,
            amount=0
        )
        return result