// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * PharmaChain — Pharmaceutical Supply Chain Smart Contract
 * =========================================================
 * Records custody events for medicine batches on the Ethereum blockchain.
 * Each actor (manufacturer, distributor, pharmacist) appends a signed
 * record when they handle a medicine batch.
 *
 * Author : Sivaranjani R
 * College : Anna University Regional Campus, Madurai
 *
 * NOTE: This contract implements basic QR-token-based provenance.
 * The QR cloning vulnerability (see README.md) exists at the
 * token layer — a copied token passes this contract's checks.
 * The TrustChain PhD proposal addresses this with ZKP authentication.
 */

contract PharmaChain {

    // Actor roles in the supply chain
    enum Actor { Manufacturer, Distributor, Pharmacist, Customer }

    // A single custody event
    struct CustodyRecord {
        address recorder;
        Actor   actor;
        uint256 timestamp;
        string  note;
    }

    // medicine_id => list of custody records
    mapping(string => CustodyRecord[]) public custodyChain;

    // Events emitted on each scan
    event CustodyRecorded(string indexed medicineId, Actor actor, address recorder);

    /**
     * Record a custody event for a medicine batch.
     * @param medicineId  The QR token assigned to the medicine batch
     * @param actor       The role of the actor recording this event
     * @param note        Optional note (e.g. "Received at pharmacy")
     */
    function recordCustody(
        string memory medicineId,
        Actor actor,
        string memory note
    ) public {
        custodyChain[medicineId].push(CustodyRecord({
            recorder  : msg.sender,
            actor     : actor,
            timestamp : block.timestamp,
            note      : note
        }));
        emit CustodyRecorded(medicineId, actor, msg.sender);
    }

    /**
     * Verify the custody chain for a medicine batch.
     * Returns true only if all 4 actors recorded in correct order.
     *
     * KNOWN VULNERABILITY: This function verifies the token, not the
     * physical product. A cloned token passes this check.
     * See README.md → "Security Vulnerability Discovered"
     */
    function verifyCustody(string memory medicineId) public view returns (bool) {
        CustodyRecord[] memory records = custodyChain[medicineId];
        if (records.length < 4) return false;

        return (
            records[0].actor == Actor.Manufacturer &&
            records[1].actor == Actor.Distributor  &&
            records[2].actor == Actor.Pharmacist   &&
            records[3].actor == Actor.Customer
        );
    }

    /**
     * Get the number of custody records for a medicine batch.
     */
    function getCustodyLength(string memory medicineId) public view returns (uint256) {
        return custodyChain[medicineId].length;
    }
}
