$(document).ready(function () {
    draw_pie_chart();
});


function generateRandomIntegerInRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function draw_pie_chart() {
    let crypto_ids = get_table_tr_ids();
    let n = generateRandomIntegerInRange(3, 9);
    let crypto_ids_for_pie = (crypto_ids.sort(() => 0.5 - Math.random())).slice(0, n);

    console.log(crypto_ids_for_pie);

    let price_arr = [];
    crypto_ids_for_pie.forEach(function () {
        price_arr.push(generateRandomIntegerInRange(10, 170));
    });

    const randColor = () => {
        return "#" + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0').toUpperCase();
    }
    let colors = [];


    crypto_ids_for_pie = crypto_ids_for_pie.map(f => { return f.toUpperCase(); });

    var options = {
        series: price_arr,
        labels: crypto_ids_for_pie,
        theme: {
            monochrome: {
                color: '#0CAFFF',
                enabled: true,
                shadeTo: 'dark',
                shadeIntensity: 0.65
            }
        },
        chart: {
            type: 'pie'
        },
        dataLabels: {
            formatter(val, opts) {
                const name = opts.w.globals.labels[opts.seriesIndex]
                return [name, val.toFixed(1) + '%']
            }
        },
        legend: {
            formatter: function (seriesName, opts) {
                return [seriesName, " - ", opts.w.globals.series[opts.seriesIndex] + '$']
            },
            show: true
        },
        responsive: [{
            breakpoint: 480,
        }]
    };

    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
}   
