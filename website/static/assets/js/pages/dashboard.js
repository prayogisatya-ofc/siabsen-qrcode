Vue.createApp({
    data() {
        return {
            grafikEl: null
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        this.getToday()
        this.getTodayGuru()
    },
    methods: {
        async getToday(){
            $.blockUI({
                message: '<div class="spinner-border text-white" role="status"></div>',
                css: {
                  backgroundColor: 'transparent',
                  border: '0'
                },
                overlayCSS: {
                  opacity: 0.5
                }
            })

            await axios.get(`/today`)
                .then(result => {
                    $.unblockUI();
                    var data = result.data
                    let newArray = []

                    for (let i = 0; i < data.labels.length; i++) {
                        newArray.push(i+1)
                    }
                    
                    var ChartConfig = {
                        chart: {
                            height: 270,
                            type: "bar",
                            toolbar: {
                                show: false,
                            },
                        },
                        plotOptions: {
                            bar: {
                                horizontal: true,
                                barHeight: "70%",
                                distributed: true,
                                startingShape: "rounded",
                                borderRadius: 7,
                            },
                        },
                        grid: {
                            strokeDashArray: 10,
                            borderColor: "#1E2139",
                            xaxis: {
                                lines: {
                                    show: true,
                                },
                            },
                            yaxis: {
                                lines: {
                                    show: false,
                                },
                            },
                            padding: {
                                top: -35,
                                bottom: -12,
                            },
                        },
                    
                        colors: [
                            "#5369F8",
                            "#25C2E3",
                            "#43D39E",
                            "#A8AAAE",
                            "#FF5C75",
                            "#FFBE0B"
                        ],
                        dataLabels: {
                            enabled: true,
                            style: {
                                colors: ["#fff"],
                                fontWeight: 200,
                                fontSize: "13px",
                                fontFamily: "Public Sans",
                            },
                            formatter: function (val, opts) {
                                return ChartConfig.labels[opts.dataPointIndex];
                            },
                            offsetX: 0,
                            dropShadow: {
                                enabled: false,
                            },
                        },
                        labels: data.labels,
                        series: [
                            {
                                data: data.series,
                            },
                        ],
                    
                        xaxis: {
                            categories: newArray.reverse(),
                            axisBorder: {
                                show: false,
                            },
                            axisTicks: {
                                show: false,
                            },
                            labels: {
                                style: {
                                    colors: "#5369F8",
                                    fontSize: "13px",
                                },
                                formatter: function (val) {
                                    return `${val}%`;
                                },
                            },
                        },
                        yaxis: {
                            max: 100,
                            labels: {
                                style: {
                                    colors: ["#5369F8"],
                                    fontFamily: "Public Sans",
                                    fontSize: "13px",
                                },
                            },
                        },
                        tooltip: {
                            enabled: true,
                            style: {
                                fontSize: "12px",
                            },
                            onDatasetHover: {
                                highlightDataSeries: false,
                            },
                            custom: function ({ series, seriesIndex, dataPointIndex, w }) {
                                return (
                                    '<div class="px-3 py-2">' +
                                    "<span>" +
                                    series[seriesIndex][dataPointIndex] +
                                    "%</span>" +
                                    "</div>"
                                );
                            },
                        },
                        legend: {
                            show: false,
                        },
                    }
                    const horizontalBarChart = new ApexCharts(this.$refs.grafikAbsensi, ChartConfig)
                    horizontalBarChart.render()
                })
                .catch(error => {
                    $.unblockUI();
                    Swal.fire({
                        icon: "warning",
                        text: "Gagal mengambil data!",
                        timer: 2000,
                        showConfirmButton: false,
                    })
                })
        },
        async getTodayGuru(){
            $.blockUI({
                message: '<div class="spinner-border text-white" role="status"></div>',
                css: {
                  backgroundColor: 'transparent',
                  border: '0'
                },
                overlayCSS: {
                  opacity: 0.5
                }
            })

            await axios.get(`/today-guru`)
                .then(result => {
                    $.unblockUI();
                    var data = result.data
                    
                    const RadialChartConfig = {
                        series: data.series,
                        labels: ['Guru Absen'],
                        chart: {
                            height: 360,
                            type: 'radialBar'
                        },
                        plotOptions: {
                            radialBar: {
                                offsetY: 10,
                                startAngle: -140,
                                endAngle: 130,
                                hollow: {
                                    size: '65%'
                                },
                                track: {
                                    background: "#ffffff",
                                    strokeWidth: '100%'
                                },
                                dataLabels: {
                                    name: {
                                        offsetY: -20,
                                        color: "#a5a3ae",
                                        fontSize: '13px',
                                        fontWeight: '400',
                                        fontFamily: 'Public Sans'
                                    },
                                    value: {
                                        offsetY: 10,
                                        color: "#5d596c",
                                        fontSize: '38px',
                                        fontWeight: '500',
                                        fontFamily: 'Public Sans'
                                    }
                                }
                            }
                        },
                        colors: ["#43D39E"],
                        fill: {
                            type: 'gradient',
                            gradient: {
                                shade: 'dark',
                                shadeIntensity: 0.5,
                                gradientToColors: ["#43D39E"],
                                inverseColors: true,
                                opacityFrom: 1,
                                opacityTo: 0.6,
                                stops: [30, 70, 100]
                            }
                        },
                        stroke: {
                            dashArray: 10
                        },
                        grid: {
                            padding: {
                                top: -20,
                                bottom: 5
                            }
                        },
                        states: {
                            hover: {
                                filter: {
                                    type: 'none'
                                }
                            },
                            active: {
                                filter: {
                                    type: 'none'
                                }
                            }
                        },
                        responsive: [
                            {
                                breakpoint: 1025,
                                options: {
                                    chart: {
                                        height: 330
                                    }
                                }
                            },
                            {
                                breakpoint: 769,
                                options: {
                                    chart: {
                                        height: 280
                                    }
                                }
                            }
                        ]
                    }
                    const RadialChart = new ApexCharts(this.$refs.grafikAbsensiGuru, RadialChartConfig)
                    RadialChart.render()
                })
                .catch(error => {
                    $.unblockUI();
                    Swal.fire({
                        icon: "warning",
                        text: "Gagal mengambil data!",
                        timer: 2000,
                        showConfirmButton: false,
                    })
                })
        }
    }
}).mount('#app')