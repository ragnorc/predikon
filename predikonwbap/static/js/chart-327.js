
var ctx = document.getElementById('plot-327').getContext('2d');
var myLineChart = new Chart(ctx, {
    type: 'line',
    // The data for our dataset
    data: {
        labels: ["12:35", "13:00", "13:30", "14:00", "15:30"],
        datasets: [
            {
                label: "Prediction",
                data: [67.45, 67.44, 67.33, 67.39, 66.59],
                fill: false,
                borderColor: "#f5593d",
                pointBorderColor: "#f5593d",
                pointBackgroundColor: "#f5593d"
            },
            {
                label: "Count",
                data: [66.99, 67.36, 67.66, 67.53, 66.45],
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
                    suggestedMin: 60,
                    suggestedMax: 70
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
