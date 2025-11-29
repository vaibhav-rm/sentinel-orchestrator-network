# backend/agents/oracle.py
import asyncio
import requests
import base64
import json
import nacl.signing
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from message_bus import MessageBus  # MEMBER1 builds this

class OracleAgent:
    def __init__(self):
        self.private_key = nacl.signing.SigningKey.generate()
        self.public_key = self.private_key.verify_key
        self.bus = MessageBus()  # Listens for your messages
        self.escrow_balance = 0.0

        # Load Sentinel's PUBLIC key (MEMBER1 shares this via config)
        # For now, placeholder - will be fixed later
        self.sentinel_public_bytes = base64.b64decode("SENTINEL_PUBLIC_BASE64_PLACEHOLDER")
        self.sentinel_verify_key = VerifyKey(self.sentinel_public_bytes)

        # Blockfrost API setup
        self.BLOCKFROST_URL = "https://cardano-mainnet.blockfrost.io/api/v0"
        self.BLOCKFROST_PROJECT_ID = "preproduDheFnsnBxApBxdqkkpnoHLelIefGX7T"  # Get from blockfrost.io

    async def start(self):
        await self.bus.subscribe("did:masumi:oracle_01", self.handle_message)

    async def handle_message(self, envelope):
        # 1. Verify signature
        if not self.verify_signature(envelope):
            return

        if envelope["type"] == "HIRE_REQUEST":
            await self.execute_fork_check(envelope)

    async def execute_fork_check(self, hire_request):
        # 2. Accept payment (virtual)
        escrow_id = hire_request["payload"]["escrow_id"]
        self.escrow_balance += hire_request["payload"]["amount"]

        # 3. Get real mainnet data
        user_tip = hire_request["payload"]["user_tip"]
        mainnet_tip = await self.fetch_mainnet_tip()

        # 4. Fork logic
        delta = abs(mainnet_tip - user_tip)
        status = "MINORITY_FORK_DETECTED" if delta > 5 else "SAFE_CHAIN"

        # 5. Reply
        reply = {
            "protocol": "IACP/2.0",
            "type": "JOB_COMPLETE",
            "from_did": "did:masumi:oracle_01",
            "payload": {
                "status": status,
                "mainnet_tip": mainnet_tip,
                "user_node_tip": user_tip,
                "evidence": "block_divergence" if delta > 5 else "none"
            }
        }
        signed_reply = self.sign_envelope(reply)
        await self.bus.publish(signed_reply)

    async def fetch_mainnet_tip(self):
        # Blockfrost call (get free key from blockfrost.io)
        headers = {"project_id": self.BLOCKFROST_PROJECT_ID}
        resp = requests.get(f"{self.BLOCKFROST_URL}/blocks/latest", headers=headers)
        resp.raise_for_status()
        return resp.json()["height"]

    def verify_signature(self, envelope):
        if "signature" not in envelope:
            return False

        # Reconstruct original message (exclude signature)
        message = {k: v for k, v in envelope.items() if k != "signature"}
        message_bytes = json.dumps(message, sort_keys=True, separators=(',', ':')).encode()

        signature_bytes = base64.b64decode(envelope["signature"])

        try:
            self.sentinel_verify_key.verify(message_bytes, signature_bytes)
            print(f"✅ Verified: {envelope['from_did']}")
            return True
        except BadSignatureError:
            print("❌ Fake signature dropped")
            return False