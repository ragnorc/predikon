var ctx = document.getElementById('plot-328').getContext('2d');
var myLineChart = new Chart(ctx, {
    type: 'line',
    // The data for our dataset
    data: {
        labels: ["12:35", "13:00", "13:30", "14:00", "15:30"],
        datasets: [
            {
                label: "Prediction",
                data: [62.12, 62.87, 63.13, 62.86, 62.22],
                fill: false,
                borderColor: "#f5593d",
                pointBorderColor: "#f5593d",
                pointBackgroundColor: "#f5593d"
            },
            {
                label: "Count",
                data: [58.50, 60.50, 61.44, 61.56, 62.51],
                fill: false,
                borderColor: "#fbc658",
                pointBorderColor: "#fbc658",
                pointBackgroundColor: "#fbc658"
            }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        // title: {
        //   display: true,
        //   text: "Prediction"
        // },
        legend: {
            display: false
        },
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    // beginAtZero: true,   // minimum value will be 0.
                    suggestedMin: 55,
                    suggestedMax: 65
                },
                gridLines: {
                    // drawOnChartArea: false,
                    display: false
                }
            }],
            xAxes: [{
                display: true,
                ticks: {
                    display: false
                },
                gridLines: {
                    // drawOnChartArea: false,
                    display: false
                },
            }]
        }
    }

});
