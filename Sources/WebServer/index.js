const bodyParser = require('body-parser');
const cors = require('cors');
const express = require('express');
const zerorpc = require("zerorpc");

const config = require('./config');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
	extended: true
}));
app.use(cors());

const predictor_client = new zerorpc.Client();
predictor_client.connect("tcp://localhost:" + config.corePort);

app.get("/predict", (req, res) => {
    predictor_client.invoke("predict", req.query, function(error, data, more) {
        res.send(data);
    });
});

app.listen(config.serverPort, function() {
	console.log('The WebServer is running...');
});