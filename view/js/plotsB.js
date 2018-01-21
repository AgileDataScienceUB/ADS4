
function call_plotsB(){
// SCATTER 1

    $.getJSON('http://34.242.186.183:3031/plotB1', function(data1) {
        //data is the JSON string
        /*alert(data1["values"][0])
        alert(data1["values"][1])
        console.log(data1);*/

        var modData3 = ['salary'];
        data1["values"][0].forEach(function(d) {
            //alert(d)
            modData3.push(d);
        });

        var results3 = ['probability_to_leave'];
        data1["values"][1].forEach(function(d) {
            results3.push(d*100);
        });

        var scatter = c3.generate({
            bindto: '#scatterB',
            data: {

            xs: {
                probability_to_leave: 'salary'
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
                    label: data1["layer-x"],
                    tick: {
                        fit: false
                    }
                },
                y: {
                    max: 90,
                    label: data1["layer-y"]
                }
            },

            legend: {
                show: false
            },
            color: {
                pattern: ['#F97600']
            },
        });

    });



    $.getJSON('http://34.242.186.183:3031/plotB2', function(data2) {
        //data is the JSON string
        var modData = [];
        data2["values"][0].forEach(function(d) {
            //alert(d)
            modData.push(d);
          });

        var results = [data2["layer-y"]];
        data2["values"][1].forEach(function(d) {
            results.push(d*100);
        });

        var barchart2 = c3.generate({
            bindto: '#barchartB',
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
                        label: data2["layer-x"],
                        type: 'category',
                        categories: modData,
                        tick: {
                            rotate: 85,
                            multiline: false
                        }
                    },
                    y: {
                        max: 90,
                        label: data2["layer-y"]
                    }
            },
            color: {
                pattern: ['#F97600']
            },
        });

    });

    $.getJSON('http://34.242.186.183:3031/plotB3', function(data3) {
        var modData33 = [];
        data3["values"][0].forEach(function(d) {
            //alert(d)
            modData33.push(d);
          });

        var results = ["Probability to leave >80% by age group"];
        data3["values"][1].forEach(function(d) {
            results.push(d*100);
        });


        var chart = c3.generate({
            bindto: '#barB',
            data: {
                columns: [
                    results
                ],
                type: 'bar',
            },
            axis: {
                    x: {
                        label: data3["layer-x"],
                        type: 'category',
                        categories: modData33,
                        tick: {
                            rotate: 85,
                            multiline: false
                        }
                    },
                    y: {
                        max: 90,
                        label: data3["layer-y"]
                    }
               },
           color: {
                pattern: ['#F97600']
            },
        });


    });



    $.getJSON('http://34.242.186.183:3031/plotB4', function(data4) {
        //data is the JSON string
        var modData = ["num"];
        data4["values"][0].forEach(function(d) {
            //alert(d)
            modData.push(d);
          });

        var results = ["x"];
        data4["values"][1].forEach(function(d) {
            results.push(d*100);
        });


        var barchart2 = c3.generate({
            bindto: '#barchartB2',
            data: {
                x: 'x',
                columns: [
                    results,
                    modData
                
            ],
                type: 'bar'
            },
            bar: {
                width: {
                    ratio: 1 // this makes bar width 50% of length between ticks
                }
            },
            axis: {
                    x: {
                        tick: {
                            values: ['10','20','25','50','75','80','90','100']
                        },
                        
                        label: "Probability of leaving",
                        max: 90,
                    },
                    y: {
                        min: 5,
                        label: "Number of employees"
                    }
            },

            color: {
                pattern: ['#F97600']
            },
            legend: {
                show: false
            },
        });

    });

    $.getJSON('http://34.242.186.183:3031/plotB5', function(data5) {

        var results = ["num"];
            data5["values"][1].forEach(function(d) {
            results.push(d*100);
        });

        var modData = ['x'];
            data5["values"][0].forEach(function(d) {
            modData.push(d);
        });


        var area_chart = c3.generate({
            bindto: '#area_chartB',
            data: {
               x: 'x',
                columns: [
                    modData,
                    results
                ],
                types: {
                    x: 'area-spline'
                },
            },
         
            legend: {
                show: false
            },
            axis: {
                x: {
                    label: data5["layer-x"],
                    tick: {
                        values: ['1','2','5','7','10','20','30']
                    },
                },
                y: {
                    max: 90,
                    label: data5["layer-y"]
                },
            },
            color: {
                pattern: ['#F97600']
            },
        });
    });

}
