function call_plotsA(){

    $.getJSON('http://34.242.186.183:3031/plotA1', function(data1) {
    //alert(data1["values"][0][0])
    var pie = c3.generate({
        bindto: '#pie',
        data: {
            // iris data from R
            columns: [
                [data1["values"][0][0], data1["values"][1][0]],
                [data1["values"][0][1], data1["values"][1][1]],
                [data1["values"][0][2], data1["values"][1][2]],
            ],
            type : 'pie',
            onclick: function (d, i) { console.log("onclick", d, i); },
            onmouseover: function (d, i) { console.log("onmouseover", d, i); },
            onmouseout: function (d, i) { console.log("onmouseout", d, i); }
        }
    });

    });

    $.getJSON('http://34.242.186.183:3031/plotA2', function(data2) {
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
    bindto: '#barchart',
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

    $.getJSON('http://34.242.186.183:3031/plotA3', function(data3) {
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
        bindto: '#scatter',
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


    $.getJSON('http://34.242.186.183:3031/plotA4', function(data4) {
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
            bindto: '#barchart2',
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
            /*
            color: {
                //ff9896
                pattern: ['#98df8a', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
            },
            */
        });
    });


    //$.getJSON('http://34.242.186.183:3031/plotA5', function(data4) {
    var area_chart = c3.generate({
        bindto: '#area_chart',
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

    var gauge = c3.generate({
        bindto: '#gauge',
        data: {
            columns: [
                ['data', 91.4]
            ],
            type: 'gauge',
            onclick: function (d, i) { console.log("onclick", d, i); },
            onmouseover: function (d, i) { console.log("onmouseover", d, i); },
            onmouseout: function (d, i) { console.log("onmouseout", d, i); }
        },
        color: {
            pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'], // the three color levels for the percentage values.
            threshold: {
                values: [30, 60, 90, 100]
            }
        },/*
        size: {
            height: 300,
            width: 100
        }*/
    });



    var gauge2 = c3.generate({
        bindto: '#gauge2',
        data: {
            columns: [
                ['data', 67.8]
            ],
            type: 'gauge',
            onclick: function (d, i) { console.log("onclick", d, i); },
            onmouseover: function (d, i) { console.log("onmouseover", d, i); },
            onmouseout: function (d, i) { console.log("onmouseout", d, i); }
        },
        color: {
            pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'], // the three color levels for the percentage values.
            threshold: {
                values: [30, 60, 90, 100]
            }
        },
        /*
        size: {
            height: 300,
            width: 100
        }*/
    });
    //});
}

