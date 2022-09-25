function get_crypto_prices_for_table() {
    var liveprice = {
        "async": true,
        "scroosDomain": true,
        "url": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Clitecoin%2Cethereum%2Cdogecoin&vs_currencies=usd",
        
        "method": "GET"
    }

    $.ajax(liveprice).done(function (response) {
        console.log(response);
        // btc.innerHTML = response.bitcoin.usd;
        // ltc.innerHTML = response.litecoin.usd;
        // eth.innerHTML = response.ethereum.usd;
        // doge.innerHTML = response.dogecoin.usd;
    });
}


$(document).ready(function () {
    get_crypto_prices_for_table();
    window.setInterval(function () {
        get_crypto_prices_for_table();
    }, 100000);
});