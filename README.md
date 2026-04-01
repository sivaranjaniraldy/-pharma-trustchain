# Pharma TrustChain — Blockchain Pharmaceutical Provenance System

## Problem
Counterfeit medicines kill an estimated 500,000 people annually in 
low/middle-income countries (WHO, 2023). In India, ~20% of the 
pharmaceutical market is falsified. Existing supply chain systems 
have no reliable way to verify medicine authenticity at the point 
of dispensing.

## What this project does
A blockchain-based chain-of-custody system for pharmaceutical 
supply chains. Every medicine batch is assigned a unique QR code 
at manufacture. Each actor in the chain (manufacturer → distributor 
→ pharmacist → customer) scans and appends a signed record to an 
immutable blockchain ledger. The final customer scan verifies 
whether the full custody chain is intact.

## Architecture
- Blockchain: Ethereum (Solidity smart contracts)
- QR generation: Python qrcode library
- Backend: Python / Flask
- Frontend: [your tech — React / HTML]
- Each scan event is recorded as a blockchain transaction
- Custody chain is verified by checking all required actors 
  have signed in correct order

## Security limitation discovered (research gap)
After building this system, I identified a critical vulnerability:
**QR codes can be physically cloned.** A counterfeiter who 
photographs or scans a legitimate QR code and reprints it on 
fake packaging will pass every verification check in this system.

This vulnerability exists in ALL existing QR-based blockchain 
pharma systems, including MediLedger and Modum. It is the 
primary research gap that my PhD proposal (TrustChain) addresses 
using zero-knowledge proof authentication.

## Proposed PhD research
See TrustChain research proposal — replacing QR codes with 
ZKP-based challenge-response authentication that is 
mathematically impossible to clone.

## Built by
Sivaranjani R — B.E. Computer Science, Anna University Regional 
Campus Madurai (Capstone project, [year])
