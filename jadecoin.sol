// SPDX-License-Identifier: MIT 
//Fabio Leandro Lapuinka
//versao
pragma solidity ^0.8.0;

contract jade_ico {

    //Numero maximo de jadecoin disponiveis no ICO
    uint public max_jade_coin = 100000;

    //Taxa de cotacao de jadecoin para o dolar
    uint public usd_to_jade_coin = 100;

    uint public total_jade_coin_bought = 0;

    //funcoes de equivalencia
    mapping(address => uint) equity_jadecoin;
    mapping(address => uint) equity_usd;

    //verificando se o investidor pode comprar jadecoin
    modifier can_buy_jadecoins(uint usd_invested) {
        require(usd_invested * usd_to_jade_coin + total_jade_coin_bought <= max_jade_coin, "Exceeds maximum Jade Coin supply");
        _;
    }
    
    //retorna o valor de investimento em jadecoin
    function equity_in_jadecoins(address investor) external view returns (uint) {
        return equity_jadecoin[investor];
    }

    //retorna o valor de investimento em dolar
    function equity_in_usd(address investor) external view returns (uint) {
        return equity_usd[investor];
    }

    //compra de jadecoin
    function buy_jadecoins(address investor, uint usd_invested) external 
    can_buy_jadecoins(usd_invested) {
        uint jade_coins_bought = usd_invested * usd_to_jade_coin;
        equity_jadecoin[investor] += jade_coins_bought;
        equity_usd[investor] = equity_jadecoin[investor] / usd_to_jade_coin;
        total_jade_coin_bought += jade_coins_bought;
    }

    //venda de jadecoins
    function sell_jade_coins(address investor, uint jadecoins_sold) external {
        require(equity_jadecoin[investor] >= jadecoins_sold, "Insufficient Jade Coins to sell");
        equity_jadecoin[investor] -= jadecoins_sold;
        equity_usd[investor] = equity_jadecoin[investor] / usd_to_jade_coin;
        total_jade_coin_bought -= jadecoins_sold;
    }
}