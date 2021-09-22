const labels_month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const chartsByCanvasId = {};
let select_year = null
$(document).ready(() => {

    chart_doughnut("user-chart", "User")

    chart_doughnut("post-chart", "Post")

    const handleChangeSelectYear = async (year) => {

        // console.log($(this))

        // console.log(year)
        let data = await fetch('dashboard/statistical-post-year/?year=' + year).then(res => res.json())

        // console.log(data.months)
        let data_month = []
        let label = Object.keys(data.months).map(k => {
            data_month.push(data.months[k])
            return labels_month[parseInt(k) - 1]
        })
        // console.log(label, data_month)
        let alpha = 0.36
        let backgroundColor = data_month.map(i => random_bg_color_rgba(alpha))
        let datasets = {
            label: year,
            data: data_month,
            backgroundColor: backgroundColor,
            borderColor: backgroundColor.map(i => i.replaceAll(alpha, 1)),
            borderWidth: 1,
            barPercentage: 0.3,
            minBarLength: 20,
        }
        // console.table(data_month,)
        let data_drawn = {
            labels: label,
            datasets: [datasets,]
        }
        let canvasid = "post-year-bar-chart"
        let option = {
            onClick: (e) => {
                handleOnClick(e, year)
            }
        }
        destroyChartIfNecessary(canvasid)
        let chart = chart_bar(canvasid, "Thống kê bài viết Năm " + year, data_drawn, option)
        registerNewChart(canvasid, chart)
    }

    select_year = $("div.legend input[name='checkbox_year']")

    let datenow = new Date()

    select_year.change(async function (e) {
        let year = e.target.value
        handleChangeSelectYear(year)
        let month = datenow.getMonth() + 1
        // console.log(year !== datenow.getFullYear().toString(), month)
        if (year !== datenow.getFullYear().toString()) {
            month = 1
        }
        draw_chart_month(year, month)
    })

    handleChangeSelectYear(datenow.getFullYear())

    draw_chart_month(datenow.getFullYear(), datenow.getMonth() + 1)
})

const get_val_checkbox_year = () => {
    return select_year.filter((k, v) => v.checked === true)[0].value
}

const destroyChartIfNecessary = (canvasId) => {
    if (chartsByCanvasId[canvasId]) {
        chartsByCanvasId[canvasId].destroy();
    }
}

const registerNewChart = (canvasId, chart) => {
    chartsByCanvasId[canvasId] = chart;
}

const random_bg_color = () => {
    const x = Math.floor(Math.random() * 256);
    const y = Math.floor(Math.random() * 256);
    const z = Math.floor(Math.random() * 256);
    return "rgb(" + x + "," + y + "," + z + ")";
}

const random_bg_color_rgba = (alpha) => {
    const x = Math.floor(Math.random() * 256);
    const y = Math.floor(Math.random() * 256);
    const z = Math.floor(Math.random() * 256);

    return "rgba(" + x + "," + y + "," + z + "," + alpha + ")";
}

const getMonthParserInt = (month) => {
    return labels_month.indexOf(month) + 1
}

const draw_chart_month = (year, month) => {
    fetch('dashboard/statistical-post-year/?year=' + year + '&month=' + month).then(res => res.json()).then(data => {
        // console.log(data.days)
        let data_days = []
        let label = Object.keys(data.days).map(k => {
            data_days.push(data.days[k])
            return "Day " + k
        })
        // console.log(label, data_days,year,month)
        let alpha = 0.36
        let backgroundColor = data_days.map(i => random_bg_color_rgba(alpha))
        let datasets = {
            label: month + " - " + year,
            data: data_days,
            backgroundColor: backgroundColor,
            borderColor: backgroundColor.map(i => i.replaceAll(alpha, 1)),


        }
        let data_drawn = {
            labels: label,
            datasets: [{
                ...datasets,
                label: "Chart Bar",
                barPercentage: 0.7,
                minBarLength: 20,
                borderWidth: 1,
            }, {
                ...datasets,
                type: 'line',
                label: 'Chart Line',
                fill: false,
                borderColor: "rgba(255,0,0,0.76)"
            }]
        }
        let canvasid = "post-month-bar-chart"
        destroyChartIfNecessary(canvasid)
        let chart = chart_bar(canvasid, "Thống kê bài viết tháng " + month + " năm " + year, data_drawn)
        registerNewChart(canvasid, chart)
    })
}

const handleOnClick = (e, year) => {
    //click Trên từng cột dữ liệu lấy dữ liệu trên cột đó
    let title = e.chart.tooltip.title[0]
    const month = getMonthParserInt(title)
    draw_chart_month(year, month)
}

const chart_doughnut = (canvans_id, label_center) => {
    let ctx = $("#" + canvans_id)
    let data = ctx.data("datasets")
    let labels
    let total = 0
    try {
        let parseTestJson = data.replaceAll("'", '"')
        data = JSON.parse(parseTestJson)
        labels = Object.keys(data)
        total = data["total"]
        let index_total = labels.indexOf("total")
        if (index_total > -1)
            labels.splice(index_total, 1)
        // console.log(labels, data)
        data = labels.map(i => data[i])
        // console.log(data)
        // console.log(total)
        if (total === undefined)
            total = data.reduce((a, b) => a + b, 0)
    } catch (e) {

    }
    // console.log(typeof data)
    let myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: data.map(i => random_bg_color()),

                }]

            },
            options: {
                plugins: {
                    legend: {
                        display: true,
                        position: 'right'
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
                        ctx.font = "20px Arial";
                        ctx.fillText(label_center.toUpperCase(), x - 28, y);
                        if (total > 100)
                            x -= 20
                        if (total < 100)
                            x -= 15
                        if (total > 1000)
                            x -= 8
                        ctx.fillText(total, x, y + 24);

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

const chart_bar = (canvans_id, str_title, data, option = {}) => {
    let ctx = $("#" + canvans_id)
    // const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    return new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'red'
                        }
                    },
                    x: {
                        // ticks: {
                        //
                        // }
                    }
                },
                plugins: {

                    legend: {
                        display: true
                    },
                    title: {
                        display: true,
                        text: str_title
                    },
                    tooltip: {
                        callbacks: {
                            footer: (bar)=>  "Tổng số bài viết: " +bar[0].raw
                            ,
                        }
                    }

                },
                ...option
            },
            plugins: [
                {
                    id: "post-month-bar-chart",
                    beforeDraw: (chart) => {
                        // console.log(canvans_id,data.datasets[0].data.length)
                        if (data.datasets[0].data.length === 0) {
                            const ctx = chart.ctx;
                            // console.log(chart)
                            const {top, left, width, height} = chart.chartArea;
                            let x = left + width / 2;
                            let y = top + height / 2;
                            // ctx.drawImage(image, x, y);
                            ctx.font = "20px Arial";
                            ctx.fillText("Tháng " + data.datasets[0].label + " không có bài viết", x - 110, y - 3);
                        }

                    }
                }
            ]
        }
    )
}

