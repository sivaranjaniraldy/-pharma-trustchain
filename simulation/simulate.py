"""
Pharma TrustChain — Supply Chain Simulation
============================================
This script simulates a blockchain-based pharmaceutical
provenance system and demonstrates the QR cloning vulnerability
that motivates the TrustChain PhD research proposal.

Author : Sivaranjani R
College : Anna University Regional Campus, Madurai
Project : Undergraduate Capstone — Counterfeit Medicine Detection
"""

import hashlib
import uuid
import json
from datetime import datetime


# ── Blockchain Ledger (simulated as a list of blocks) ────────────────────────

class Block:
    def __init__(self, index, data, previous_hash):
        self.index         = index
        self.timestamp     = datetime.now().isoformat()
        self.data          = data
        self.previous_hash = previous_hash
        self.hash          = self._compute_hash()

    def _compute_hash(self):
        content = json.dumps({
            "index"         : self.index,
            "timestamp"     : self.timestamp,
            "data"          : self.data,
            "previous_hash" : self.previous_hash,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def __repr__(self):
        return (f"Block #{self.index} | Actor: {self.data['actor']:<14} "
                f"| Hash: {self.hash[:12]}... | Prev: {self.previous_hash[:12]}...")


class PharmaLedger:
    """Simulated blockchain ledger for pharmaceutical custody chain."""

    def __init__(self):
        genesis = Block(0, {"actor": "GENESIS", "medicine_id": None, "note": "Chain start"}, "0" * 64)
        self.chain = [genesis]

    def add_record(self, actor, medicine_id, note=""):
        prev_hash = self.chain[-1].hash
        block = Block(len(self.chain), {
            "actor"      : actor,
            "medicine_id": medicine_id,
            "note"       : note,
        }, prev_hash)
        self.chain.append(block)
        return block

    def verify_custody(self, medicine_id):
        """
        Verify the full custody chain for a medicine batch.
        Returns True only if all 4 required actors scanned in correct order.
        """
        required_actors = ["MANUFACTURER", "DISTRIBUTOR", "PHARMACIST", "CUSTOMER"]
        found = [
            b.data["actor"]
            for b in self.chain
            if b.data.get("medicine_id") == medicine_id
        ]
        return found == required_actors

    def print_chain(self):
        print("\n  Blockchain Ledger:")
        print("  " + "-" * 70)
        for block in self.chain:
            print(f"  {block}")
        print("  " + "-" * 70)


# ── QR Code Identity (simulated as a unique token string) ────────────────────

def generate_qr_identity(medicine_name, batch_number):
    """
    In a real system this would generate a scannable QR image.
    Here we simulate it as a unique token — the medicine's digital identity.
    """
    raw = f"{medicine_name}::{batch_number}::{uuid.uuid4()}"
    token = hashlib.sha256(raw.encode()).hexdigest()[:24]
    return token


# ── Simulation ────────────────────────────────────────────────────────────────

def run_legitimate_scenario(ledger, medicine_id):
    """Scenario 1: Legitimate medicine going through the full supply chain."""
    print("\n" + "=" * 60)
    print("  SCENARIO 1 — Legitimate medicine")
    print("=" * 60)

    print(f"\n  Medicine ID (QR token): {medicine_id}")

    print("\n  Step 1: Manufacturer registers the medicine...")
    ledger.add_record("MANUFACTURER", medicine_id, "Batch manufactured and QR assigned")

    print("  Step 2: Distributor scans and forwards...")
    ledger.add_record("DISTRIBUTOR", medicine_id, "Received and dispatched to pharmacy")

    print("  Step 3: Pharmacist scans on receipt...")
    ledger.add_record("PHARMACIST", medicine_id, "Received in pharmacy stock")

    print("  Step 4: Customer scans to verify...")
    ledger.add_record("CUSTOMER", medicine_id, "Customer verification scan")

    ledger.print_chain()

    result = ledger.verify_custody(medicine_id)
    print(f"\n  Verification result: {'✓ AUTHENTIC — full custody chain verified' if result else '✗ SUSPICIOUS'}")
    return result


def run_cloning_attack_scenario(ledger, medicine_id):
    """
    Scenario 2: The QR Cloning Attack.

    A counterfeiter photographs the QR code from the legitimate medicine
    and prints it on a fake packet. Since the QR token is static,
    the fake packet carries the IDENTICAL token.

    The current system CANNOT distinguish the clone from the original.
    This is the core vulnerability that TrustChain's ZKP layer solves.
    """
    print("\n" + "=" * 60)
    print("  SCENARIO 2 — QR Cloning Attack (the vulnerability)")
    print("=" * 60)

    cloned_id = medicine_id   # <-- same token, printed on a FAKE packet

    print(f"\n  Attacker clones QR token: {cloned_id}")
    print("  (Identical to the legitimate medicine — system cannot tell them apart)")

    print("\n  Fake packet enters a DIFFERENT pharmacy...")
    second_ledger = PharmaLedger()
    second_ledger.add_record("MANUFACTURER", cloned_id, "** THIS RECORD IS FROM THE REAL MEDICINE **")
    second_ledger.add_record("DISTRIBUTOR",  cloned_id, "** CLONED — counterfeiter inserted here **")
    second_ledger.add_record("PHARMACIST",   cloned_id, "Pharmacist scan — clone undetected")
    second_ledger.add_record("CUSTOMER",     cloned_id, "Customer scans fake packet")

    second_ledger.print_chain()

    result = second_ledger.verify_custody(cloned_id)
    print(f"\n  Verification result: {'✓ AUTHENTIC' if result else '✗ SUSPICIOUS'} "
          f"<-- WRONG! This is a FAKE medicine but system says authentic!")

    print("\n  ROOT CAUSE:")
    print("  Static QR tokens can be copied. The blockchain only")
    print("  verifies the token, NOT the physical product.")
    print("\n  PROPOSED SOLUTION (TrustChain PhD research):")
    print("  Replace static QR with Zero-Knowledge Proof authentication.")
    print("  Each scan issues a fresh cryptographic challenge.")
    print("  A cloned token CANNOT answer a fresh challenge — verification fails.")


def run_incomplete_chain_scenario(ledger_ref):
    """
    Scenario 3: Distributor skips the scan (partial custody chain).
    Demonstrates anomaly detection use case for the federated learning layer.
    """
    print("\n" + "=" * 60)
    print("  SCENARIO 3 — Incomplete custody chain (anomaly detection)")
    print("=" * 60)

    incomplete_id = generate_qr_identity("Paracetamol-500mg", "BATCH-999")
    skip_ledger   = PharmaLedger()

    print(f"\n  Medicine ID: {incomplete_id}")
    print("\n  Manufacturer scans... Distributor SKIPS scan... Pharmacist scans...")

    skip_ledger.add_record("MANUFACTURER", incomplete_id, "Manufactured OK")
    # DISTRIBUTOR deliberately skips
    skip_ledger.add_record("PHARMACIST",   incomplete_id, "Received — but distributor scan missing!")
    skip_ledger.add_record("CUSTOMER",     incomplete_id, "Customer scan")

    skip_ledger.print_chain()

    result = skip_ledger.verify_custody(incomplete_id)
    print(f"\n  Verification result: {'✓ AUTHENTIC' if result else '✗ SUSPICIOUS — missing distributor scan'}")
    print("\n  This pattern (missing custody step) is detectable by the")
    print("  anomaly detection layer in TrustChain's federated learning system.")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PHARMA TRUSTCHAIN — Supply Chain Simulation")
    print("  Sivaranjani R | Anna University Regional Campus Madurai")
    print("=" * 60)

    ledger      = PharmaLedger()
    medicine_id = generate_qr_identity("Amoxicillin-250mg", "BATCH-2024-001")

    run_legitimate_scenario(ledger, medicine_id)
    run_cloning_attack_scenario(ledger, medicine_id)
    run_incomplete_chain_scenario(ledger)

    print("\n" + "=" * 60)
    print("  Simulation complete.")
    print("  See README.md for research context and PhD proposal.")
    print("=" * 60 + "\n")
