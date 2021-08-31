$(document).ready(() => {
    chart_doughnut("user-chart")
})


var randomScalingFactor = function () {
    return Math.round(Math.random() * 1000)
};

var lineChartData = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        },
        {
            label: "My Second dataset",
            fillColor: "rgba(48, 164, 255, 0.2)",
            strokeColor: "rgba(48, 164, 255, 1)",
            pointColor: "rgba(48, 164, 255, 1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(48, 164, 255, 1)",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]

}

var barChartData = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        },
        {
            fillColor: "rgba(48, 164, 255, 0.2)",
            strokeColor: "rgba(48, 164, 255, 0.8)",
            highlightFill: "rgba(48, 164, 255, 0.75)",
            highlightStroke: "rgba(48, 164, 255, 1)",
            data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
        }
    ]

}

var pieData = [
    {
        value: 300,
        color: "#30a5ff",
        highlight: "#62b9fb",
        label: "Blue"
    },
    {
        value: 50,
        color: "#ffb53e",
        highlight: "#fac878",
        label: "Orange"
    },
    {
        value: 100,
        color: "#1ebfae",
        highlight: "#3cdfce",
        label: "Teal"
    },
    {
        value: 120,
        color: "#f9243f",
        highlight: "#f6495f",
        label: "Red"
    }

];

var doughnutData = [
    {
        value: 300,
        color: "#30a5ff",
        highlight: "#62b9fb",
        label: "Blue"
    },
    {
        value: 50,
        color: "#ffb53e",
        highlight: "#fac878",
        label: "Orange"
    },
    {
        value: 100,
        color: "#1ebfae",
        highlight: "#3cdfce",
        label: "Teal"
    },
    {
        value: 120,
        color: "#f9243f",
        highlight: "#f6495f",
        label: "Red"
    }

];


const chart_doughnut = (canvans_id) => {
    let ctx = $("#" + canvans_id)
    let data = ctx.data("datasets")
    let labels


    const image = new Image();
    image.src = 'https://www.chartjs.org/img/chartjs-logo.svg';
    try {
        let parseTestJson = data.replaceAll("'", '"')
        data = JSON.parse(parseTestJson)
        labels = Object.keys(data)
        console.log(labels, data)
        data = labels.map(i => data[i])
        console.log(data)

    } catch (e) {

    }
    console.log(typeof data)
    let myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: 'My First Dataset',
                    data: data,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)'
                    ],
                    // hoverOffset: 4
                }]

            },
            options: {
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                },
                animation: {
                    animateScale: true
                },
                responsive: false,


                // scales: {
                //     y: {
                //         beginAtZero: true
                //     }
                // }
            },
            plugins: [
                {
                    id: 'user-chart',
                    beforeDraw: (chart) => {
                        const ctx = chart.ctx;
                        const {top, left, width, height} = chart.chartArea;
                        let x = left + width / 2;
                        let y = top + height / 2;
                        // ctx.drawImage(image, x, y);



                        let total = chart.data.datasets[0].data.reduce((a, b) => a + b, 0)

                        ctx.font = "20px Arial";
                        ctx.fillText("USER", x - 30, y);
                        if (total> 100)
                            x -= 20
                        if( total< 100)
                            x -= 15
                        if (total >1000)
                            x-= 8
                        ctx.fillText(total, x, y+24);

                    }

                },

                // tooltip: {
                //     callbacks: {
                //         label: (context) => {
                //             let label = context.dataset.data[0] || '0';
                //             label += " USERS"
                //             return label;
                //         }
                //     }
                // }
            ]
        }
    )
}


