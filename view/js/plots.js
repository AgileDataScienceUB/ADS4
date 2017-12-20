d3.json("sample.json", function(data) {
  var modData = [];
  console.log(data);
  data.results.forEach(function(d, i) {
    var item = ["param-" + d.param];
    d.val.forEach(function(j) {
      item.push(j);
    });
    modData.push(item);
  });
  var pie = c3.generate({
    data: {
      xs: {
        'param-y':'param-x'
      },
      columns: modData,
      type : 'pie',
      onclick: function (d, i) { console.log("onclick", d, i); },
      onmouseover: function (d, i) { console.log("onmouseover", d, i); },
      onmouseout: function (d, i) { console.log("onmouseout", d, i); }
    }
  });
});