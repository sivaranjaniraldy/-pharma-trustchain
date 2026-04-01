# Pharma TrustChain

**Blockchain-based pharmaceutical provenance system with QR cloning vulnerability demonstration**

> Undergraduate Capstone Project — Sivaranjani R  
> B.E. Computer Science and Engineering  
> Anna University Regional Campus, Madurai

---

## The Problem

According to the WHO (2023), **1 in 10 medicines** in low and middle-income countries is substandard or falsified. In India, an estimated **20% of the pharmaceutical market** contains counterfeit products — contributing to treatment failures, antimicrobial resistance, and preventable deaths.

The supply chain that moves medicine from manufacturer to patient has no reliable, tamper-evident mechanism to verify authenticity at every handoff.

---

## What This Project Does

A blockchain-based chain-of-custody system for pharmaceutical supply chains. Every medicine batch is assigned a unique QR code at manufacture. Each actor in the chain must scan and append a signed record to an immutable ledger:

```
Manufacturer → Distributor → Pharmacist → Customer
```

When the customer scans the QR code, the system verifies whether the **complete custody chain** is intact. If any step is missing or out of order, the medicine is flagged as suspicious.

---

## Architecture

```
pharma-trustchain/
├── simulation/
│   └── simulate.py        # Python simulation of the full supply chain
├── contracts/
│   └── PharmaChain.sol    # Ethereum smart contract (Solidity)
├── docs/
│   └── architecture.md    # System design and flow diagrams
└── README.md
```

| Component | Technology |
|-----------|-----------|
| Blockchain ledger | Ethereum (Solidity smart contracts) |
| QR identity | SHA-256 token (simulated) |
| Custody simulation | Python 3 |
| Block structure | Hash-chained records with actor + timestamp |

---

## Running the Simulation

No installation required beyond Python 3.

```bash
git clone https://github.com/sivaranjaniraldy/-pharma-trustchain.git
cd pharma-trustchain
python simulation/simulate.py
```

The simulation runs three scenarios:
1. **Legitimate medicine** — full custody chain verified ✓
2. **QR cloning attack** — fake medicine passes verification (the vulnerability)
3. **Incomplete chain** — missing distributor scan flagged as anomaly

---

## Security Vulnerability Discovered

After building this system, I identified a **critical architectural flaw** present in all existing QR-based blockchain pharmaceutical systems, including MediLedger and Modum:

### The QR Cloning Attack

```
Legitimate medicine:  [QR: abc123] → Manufacturer → Distributor → Pharmacist → Customer ✓
                              |
                              | Counterfeiter photographs QR code
                              ↓
Fake medicine:        [QR: abc123] → ... → Customer ✓  ← WRONG! System says authentic!
```

**A counterfeiter who photographs or copies a legitimate QR code and reprints it on a fake packet will pass every verification check in this system.**

The blockchain only verifies the *token* — it cannot verify the *physical product*. This is the fundamental unsolved problem in pharmaceutical supply chain security.

---

## Proposed Research Extension — TrustChain PhD

This vulnerability motivates my PhD research proposal: **TrustChain**.

### Layer 1 — Zero-Knowledge Proof Authentication
Replace static QR codes with a ZKP-based challenge-response protocol embedded in an NFC chip on the packaging. Each scan issues a **fresh cryptographic challenge** — even a perfect copy of the QR token cannot answer a fresh challenge, so cloning attacks fail.

### Layer 2 — Federated Learning for Demand Forecasting
Train medicine demand models across distributed pharmacy networks **without centralising patient data** — using federated learning to predict stockouts while preserving privacy.

**Research question:** *"How can we design a pharmaceutical supply chain system that is simultaneously resistant to cryptographic cloning attacks (via ZKP) and capable of privacy-preserving demand prediction (via federated learning), deployable in low-connectivity environments across South and Southeast Asia?"*

---

## Research Context

- **Target**: SINGA PhD Scholarship — NUS / NTU / SMU / SUTD
- **Domain**: Distributed systems, cryptography, healthcare data engineering
- **Full proposal**: Available on request

---

## Author

**Sivaranjani R**  
B.E. Computer Science and Engineering  
Anna University Regional Campus, Madurai | CGPA: 7.87 / 10.0  
