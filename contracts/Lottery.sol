// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    address payable[] public players;
    uint256 internal usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE lottery_state;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10 ** 18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
    }
    /**
     * user enters lottery by paying minimal entrance fee
     */
    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery is not started");
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        players.push(msg.sender);
    }
    /**
     * user can check out the entrance fee lottery
     */
    function getEntranceFee() public view returns (uint256) {
        (,int price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * (10 ** 10);
        //now has 18 decimals
        uint256 constToEnter = (usdEntryFee * (10 ** 18)) / adjustedPrice;
        return constToEnter;
    }

    // admin can start the lotter
    function startLottery() public {}
    // admin ends the lottery and a random user gets the pot
    function endLottery() public {}
}
