
// SCATTER 1
$.getJSON('http://34.242.186.183:3031/plotB1', function(data3) {
    //data is the JSON string
    //alert(data3["values"][0])
    //alert(data3["values"][1])

    var modData3 = ['salary'];
    data3["values"][0].forEach(function(d) {
        //alert(d)
        modData3.push(d);
    });

    var results3 = ['lenght'];
    data3["values"][1].forEach(function(d) {
        results3.push(d);
    });

    var scatter = c3.generate({
        bindto: '#scatterB',
        data: {

        xs: {
            salary: 'lenght'
        },
        // iris data from R
        columns: [
            results3,
            modData3
            
        ],
        type: 'scatter'
        },
        axis: {
            x: {
                label: data3["layer-y"],
                tick: {
                    fit: false
                }
            },
            y: {
                label: data3["layer-x"]
            }
        },

        legend: {
            show: false
        },
    });

});


$.getJSON('http://34.242.186.183:3031/plotB2', function(data2) {
    //data is the JSON string
    //alert(data2["values"][0])
    //alert(data2["values"][1])

    var modData2 = ['x'];
    data2["values"][0].forEach(function(d) {
        //alert(d)
        modData2.push(d);
    });

    var results2 = [data2["layer-y"]];
    data2["values"][1].forEach(function(d) {
        results2.push(d);
    });

    //alert(results2)
    var barchart = c3.generate({
    bindto: '#barchartB',
    data: {

        x: 'x',
        columns: [

            modData2,
            results2
        ],
        type: 'bar'
    },
    bar: {
        width: {
            ratio: 0.3 // this makes bar width 50% of length between ticks
        }
        // or
        //width: 100 // this makes bar width 100px
    },
    
     axis: {
            rotated: true,
            x: {
                label: data2["layer-x"],
                tick: {
                    values: ['1000', '2500', '5000','7500','10000','12500','15000','17500','20000'],
                    rotate: 85,
                    multiline: false
                }

            },
            y: {
                max: 300,
                label: data2["layer-y"]
            }
    
    },
    });

});

$.getJSON('http://34.242.186.183:3031/plotB3', function(data4) {
    var chart = c3.generate({
        data: {
            columns: [
                ['data1', -30, 200, 200, 400, -150, 250],
                ['data2', 130, 100, -100, 200, -150, 50],
                ['data3', -230, 200, 200, -300, 250, 250]
            ],
            type: 'bar',
            groups: [
                ['data1', 'data2']
            ]
        },
        grid: {
            y: {
                lines: [{value:0}]
            }
        }
    });

    setTimeout(function () {
        chart.groups([['data1', 'data2', 'data3']])
    }, 1000);

    setTimeout(function () {
        chart.load({
            columns: [['data4', 100, -50, 150, 200, -300, -100]]
        });
    }, 1500);

    setTimeout(function () {
        chart.groups([['data1', 'data2', 'data3', 'data4']])
    }, 2000);
});



$.getJSON('http://34.242.186.183:3031/plotB4', function(data4) {
    //data is the JSON string
    //alert(data4["values"][0][0])
    //alert(data4["values"][0][1])
    var modData = [];
    data4["values"][0].forEach(function(d) {
        //alert(d)
        modData.push(d);
      });

    var results = [data4["layer-y"]];
    data4["values"][1].forEach(function(d) {
        results.push(d);
      });

    var barchart2 = c3.generate({
    bindto: '#barchartB2',
    data: {
        columns: [
            results
            //data4["values"][1][0], data4["values"][1][1], data4["values"][1][2]]
        ],
        type: 'bar'
    },
    bar: {
        width: {
            ratio: 0.8 // this makes bar width 50% of length between ticks
        }
        // or
        //width: 100 // this makes bar width 100px
    },
    axis: {
            x: {
                label: data4["layer-x"],
                type: 'category',
                categories: modData,
                tick: {
                    rotate: 85,
                    multiline: false
                }
            },
            y: {
                max: 20,
                label: data4["layer-y"]
            }
    },

    color: {
        //ff9896
        pattern: ['#98df8a', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
    },
    });
});

$.getJSON('http://34.242.186.183:3031/plotB5', function(data4) {
    var area_chart = c3.generate({
        bindto: '#area_chartB',
        data: {
            columns: [
                ['data1', 300, 350, 300, 0, 0, 0],
            ],
            types: {
                data1: 'area-spline'
            }
        },
            legend: {
                show: false
            },
    });
});
