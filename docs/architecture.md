# System Architecture — Pharma TrustChain

## Supply chain flow

```
[Manufacturer]
    |
    | 1. Generate unique QR token for medicine batch
    | 2. Call recordCustody(medicineId, MANUFACTURER)
    |
    v
[Distributor]
    |
    | 1. Scan QR code
    | 2. Call recordCustody(medicineId, DISTRIBUTOR)
    |
    v
[Pharmacist]
    |
    | 1. Scan QR code on receipt
    | 2. Call recordCustody(medicineId, PHARMACIST)
    |
    v
[Customer]
    |
    | 1. Scan QR code to verify
    | 2. System calls verifyCustody(medicineId)
    | 3. Result: AUTHENTIC (all 4 actors present in order)
    |            or SUSPICIOUS (chain incomplete or out of order)
```

## Blockchain data model

Each custody event is stored as a block containing:
- `recorder` — Ethereum address of the actor
- `actor` — role (Manufacturer / Distributor / Pharmacist / Customer)
- `timestamp` — block timestamp
- `note` — optional free text

## Known vulnerability — QR cloning attack

The system verifies the QR *token*, not the *physical product*.

```
Real medicine:  Token = "abc123" → Full chain recorded → AUTHENTIC ✓
                          |
                          | Counterfeiter copies token
                          ↓
Fake medicine:  Token = "abc123" → Full chain recorded → AUTHENTIC ✓  ← WRONG
```

## Proposed solution — TrustChain ZKP layer

Replace the static QR token with a Zero-Knowledge Proof circuit:

```
Medicine batch → NFC chip with private key k
Blockchain    → Public commitment C(k) registered at manufacture

Each scan:
  Verifier generates random challenge r
  NFC chip computes ZKP: "I know k such that C(k) is registered, 
                          given challenge r"
  Proof is verified on-chain

Clone attack:
  Attacker has token but NOT private key k
  Cannot compute valid ZKP for fresh challenge r
  Verification FAILS → medicine flagged as fake ✓
```

## Federated learning demand layer

```
Pharmacy A  Pharmacy B  Pharmacy C  ...  Pharmacy N
    |            |            |                |
    | Local      | Local      | Local          | Local
    | model      | model      | model          | model
    | training   | training   | training       | training
    |            |            |                |
    +------------+------------+----------------+
                 |
                 | Weight updates only (no raw patient data shared)
                 v
          Aggregation server
          (FedAvg algorithm)
                 |
                 v
          Global demand model
          distributed back to all pharmacies
```

This architecture forecasts medicine demand without centralising
patient dispensing data — preserving privacy while enabling
intelligent stock management.
