$(document).ready(function () {
    draw_pie_chart();
});

function draw_pie_chart() {
    var options = {
        series: values,
        labels: labels,
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
        tooltip: {
            y: {
                formatter: function(value) {
                  return value + ' $'
                }
              }
        },
        dataLabels: {
            formatter(val, opts) {
                const name = opts.w.globals.labels[opts.seriesIndex]
                return [name, val.toFixed(1) + '%']
            },
            enabled: true,
            style: {
              fontSize: "15px",
              fontFamily: "Helvetica, Arial, sans-serif",
              fontWeight: "bold"
            }
        },
        plotOptions: {
            pie: {
              dataLabels: {
                 offset: -5
               }
            }
         },
        legend: {
            formatter: function (seriesName, opts) {
                return [seriesName, " - ", opts.w.globals.series[opts.seriesIndex] + ' $']
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
