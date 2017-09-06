const express = require('express');
const bodyParser = require('body-parser');
const middleware = require('./middleware');
const http = require('http');
const cors = require('cors');
const morgan = require('morgan');
const mongoose = require('mongoose');
const config = require('./config');

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

app.post('/', middleware.auth, function (req, res) {
  const name = req.body['name'];

  console.log(`request body name attribute: ${name}`);

  res.json({message: 'post / called'})
});

module.exports = {
  app: app,
  start: function (callback) {
    mongoose.Promise = global.Promise;
    mongoose.connect('mongodb://localhost/myapp', {
      useMongoClient: true
    })
      .then(function () {
        const port = config[config.env].port;

        http.createServer(app).listen(port, function () {
          if (callback) {
            callback(port);
          }
        });
      })
      .catch(function (error) {
        console.log(error);
      });
  }
};
