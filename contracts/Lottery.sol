// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;
    uint256 internal usdEntryFee;
    AggragatorV3Interface internal ethUsdPriceFeed;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10 ** 18);
        ethUsdPriceFeed = AggragatorV3Interface(_priceFeedAddress);
    }
    // user enters lottery
    function enter() public payable {
        // TODO: check if sent at least the minium $50
        players.push(msg.sender);
    }
    /**
     * user can check out the entrance fee lottery
     */
    function getEntranceFee() public view returns (uint256) {
        (,int price,,,) = priceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10 ** 10; //now has 18 decimals

        uint256 constToEnter = (usdEntryFee ** 10 * 18) / adjustedPrice;
        return constToEnter;
    }

    // admin can start the lotter
    function startLottery() public {}
    // admin ends the lottery and a random user gets the pot
    function endLottery() public {}
}
