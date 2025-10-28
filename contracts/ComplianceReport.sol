// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ComplianceReport {
    event ReportSubmitted(address indexed sender, string message, uint256 timestamp);

    function submitReport(string memory message) public {
        emit ReportSubmitted(msg.sender, message, block.timestamp);
    }
}
