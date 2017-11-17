$(document).ready(function() {
    $("#prediction-messi-button").click(function() {
        $.get("http://localhost:8080/predict", function(data, status) {
            $("#prediction-messi").text(data)
        });
    });
});

$(document).ready(function() {
    $("#prediction-brunetta-button").click(function() {
        $.get("http://localhost:8080/predict", function(data, status) {
            $("#prediction-brunetta").text(data)
        });
    });
});

$(document).ready(function() {
    $("#prediction-ventura-button").click(function() {
        $.get("http://localhost:8080/predict", function(data, status) {
            $("#prediction-ventura").text(data)
        });
    });
});

$(document).ready(function() {
    $("#prediction-marchiori-button").click(function() {
        $.get("http://localhost:8080/predict", function(data, status) {
            $("#prediction-marchiori").text(data)
        });
    });
});

$(document).ready(function() {
    $("#prediction-rossi-button").click(function() {
        $.get("http://localhost:8080/predict", function(data, status) {
            $("#prediction-rossi").text(data)
        });
    });
});