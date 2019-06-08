
var ctx = document.getElementById('plot-326').getContext('2d');
var myLineChart = new Chart(ctx, {
    type: 'line',
    // The data for our dataset
    data: {
        labels: ["12:05", "12:30", "13:00", "14:00", "15:30"],
        datasets: [
            {
                label: "Prediction",
                data: [35.30, 35.52, 35.73, 35.45, 35.58],
                fill: false,
                borderColor: "#f5593d",
                pointBorderColor: "#f5593d",
                pointBackgroundColor: "#f5593d"
            },
            {
                label: "Count",
                data: [32.08, 33.15, 33.97, 34.46, 35.52],
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
                    suggestedMin: 30,
                    suggestedMax: 40
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
