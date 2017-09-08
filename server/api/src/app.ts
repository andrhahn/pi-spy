const express = require('express');
const bodyParser = require('body-parser');
const auth = require('./middleware/auth');
const http = require('http');
const cors = require('cors');
const morgan = require('morgan');
const mongoose = require('mongoose');
const config = require('./config');
const Device = require('./model/device');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.use(cors({
  origin: new RegExp(config[config.env].cors.origin),
  credentials: true
}));

if (config[config.env].logging.enabled) {
  app.use(morgan(config[config.env].logging.format));
}

app.get('/', function (req, res) {
  res.json({message: 'get / called'})
});

app.get('/devices', auth, function (req, res) {
  Device.find({})
    .then((devices) => {
      console.log(`Found devices: ${JSON.stringify(devices)}`);

      res.json(devices);
    })
    .catch((err) => {
      console.log('Error occurred finding devices');
    });
});

app.post('/devices', auth, function (req, res) {
  Device.create(req.body)
    .then((device) => {
      console.log(`Created device: ${JSON.stringify(device)}`);

      res.json(device);
    })
    .catch((err) => {
      console.log('Error occurred creating device');
    });
});

app.post('/', auth, function (req, res) {
  const name = req.body['name'];

  console.log(`request body name attribute: ${name}`);

  res.json({message: 'post / called'})
});

mongoose.Promise = global.Promise;
mongoose.connect(config[config.env].db.uri, { useMongoClient: true })
  .then(function () {
    const port = config[config.env].port;

    http.createServer(app).listen(port, function () {
      console.log(`Server started on port: ${port}`);
    });
  })
  .catch(function (error) {
    console.log('Error connecting to database: ' + error);
  });
