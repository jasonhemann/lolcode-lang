// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Timelock {
    address public owner;
    uint256 public lockDuration;
    mapping(address => uint256) public deposits;
    mapping(address => bool) public disputed;

    event FundsDeposited(address indexed payer, uint256 amount);
    event FundsReleased(address indexed recipient, uint256 amount);
    event DisputeRaised(address indexed payer);

    modifier onlyOwner() {
        require(msg.sender == owner, "Timelock: caller is not the owner");
        _;
    }

    modifier notDisputed(address _payer) {
        require(!disputed[_payer], "Timelock: funds are disputed");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setTimelock(uint256 _duration) external onlyOwner {
        lockDuration = _duration;
    }

    function depositFunds() external payable {
        deposits[msg.sender] += msg.value;
        emit FundsDeposited(msg.sender, msg.value);
    }

    function releaseFunds() external {
        require(block.timestamp >= lockDuration, "Timelock: funds are still locked");
        uint256 amount = deposits[msg.sender];
        require(amount > 0, "Timelock: no funds to release");

        deposits[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
        emit FundsReleased(msg.sender, amount);
    }

    function dispute() external {
        disputed[msg.sender] = true;
        emit DisputeRaised(msg.sender);
    }

    function refund() external {
        require(disputed[msg.sender], "Timelock: no dispute raised");
        uint256 amount = deposits[msg.sender];
        require(amount > 0, "Timelock: no funds to refund");

        deposits[msg.sender] = 0;
        disputed[msg.sender] = false;
        payable(msg.sender).transfer(amount);
    }
}
