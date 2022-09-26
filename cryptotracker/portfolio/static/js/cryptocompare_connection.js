function get_toplist_by_market_cap(crypto_symbols) {
    let liveprice = {
        "async": true,
        "scroosDomain": true,
        "url": "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + crypto_symbols + "&tsyms=USD",
        "method": "GET"
    }

    $.ajax(liveprice).done(function (response) {
        $.each(response["DISPLAY"], function (crypto, data) {
            let fadeOuttime = 30;
            let fadeIntime = 150;
            $("#" + crypto.toLowerCase() + "_price").fadeOut(fadeOuttime);
            $("#" + crypto.toLowerCase() + "_price").text(data["USD"]["PRICE"].replace("$ ", "") + " $");
            $("#" + crypto.toLowerCase() + "_price").fadeIn(fadeIntime);

            $("#" + crypto.toLowerCase() + "_marketcap").fadeOut(fadeOuttime);
            $("#" + crypto.toLowerCase() + "_marketcap").text(data["USD"]["MKTCAP"].replace("$ ", ""));
            $("#" + crypto.toLowerCase() + "_marketcap").fadeIn(fadeIntime);

            $("#" + crypto.toLowerCase() + "_change1h").fadeOut(fadeOuttime);
            $("#" + crypto.toLowerCase() + "_change1h").text(data["USD"]["CHANGEPCTHOUR"] + " %");
            if (data["USD"]["CHANGEPCTHOUR"] > 0) {
                $("#" + crypto.toLowerCase() + "_change1h").css("color", "green");
            } else if (data["USD"]["CHANGEPCTHOUR"] < 0) {
                $("#" + crypto.toLowerCase() + "_change1h").css("color", "red");
            } else {
                $("#" + crypto.toLowerCase() + "_change1h").css("color", "grey");
            }
            $("#" + crypto.toLowerCase() + "_change1h").fadeIn(fadeIntime);

            $("#" + crypto.toLowerCase() + "_change24h").fadeOut(fadeOuttime);
            $("#" + crypto.toLowerCase() + "_change24h").text(data["USD"]["CHANGEPCT24HOUR"] + " %");
            if (data["USD"]["CHANGEPCTHOUR"] > 0) {
                $("#" + crypto.toLowerCase() + "_change24h").css("color", "green");
            } else if (data["USD"]["CHANGEPCTHOUR"] < 0) {
                $("#" + crypto.toLowerCase() + "_change24h").css("color", "red");
            } else {
                $("#" + crypto.toLowerCase() + "_change24h").css("color", "grey");
            }
            $("#" + crypto.toLowerCase() + "_change24h").fadeIn(fadeIntime);
        });

    });
}

function get_table_tr_ids() {
    let arr = [];
    $("#toplist_by_market_cap tr").each(function () {
        arr.push(this.id);
    });
    return arr.toString();
}

$(document).ready(function () {

    let crypto_ids = get_table_tr_ids();
    get_toplist_by_market_cap(crypto_ids);
    window.setInterval(function () {
        get_toplist_by_market_cap(crypto_ids);
    }, 15000);
});
