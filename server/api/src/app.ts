const express = require('express');
const bodyParser = require('body-parser');
const auth = require('./middleware/auth');
const http = require('http');
const cors = require('cors');
const morgan = require('morgan');
const mongoose = require('mongoose');
const config = require('./config');
const Device = require('./model/device');
const User = require('./model/user');

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

app.get('/users', auth, function (req, res) {
  User.find({})
    .then((users) => {
      if (users) {
        console.log(`User found: ${JSON.stringify(users)}`);

        res.json(users);
      } else {
        const message = 'Users not found';

        console.log(message);

        res.status(404).json({message: message});
      }
    })
    .catch((err) => {
      const message = 'Error occurred finding users';

      console.log(message);

      res.status(500).json({message: message});
    });
});

app.get('/devices', auth, function (req, res) {
  Device.find({})
    .then((devices) => {
      if (devices) {
        console.log(`Devices found: ${JSON.stringify(devices)}`);

        res.json(devices);
      } else {
        const message = 'Devices not found';

        console.log(message);

        res.status(404).json({message: message});
      }
    })
    .catch((err) => {
      const message = 'Error occurred finding devices';

      console.log(message);

      res.status(500).json({message: message});
    });
});

app.get('/devices/:id', auth, function (req, res) {
  Device.findOne({_id: req.params.id})
    .then((device) => {
      if (device) {
        console.log(`Device found: ${JSON.stringify(device)}`);

        res.json(device);
      } else {
        const message = 'Device not found';

        console.log(message);

        res.status(404).json({message: message});
      }
    })
    .catch((err) => {
      const message = 'Error occurred finding device';

      console.log(message);

      res.status(500).json({message: message});
    });
});

app.post('/devices', auth, function (req, res) {
  Device.create(req.body)
    .then((device) => {
      console.log(`Device created: ${JSON.stringify(device)}`);

      res.json(device);
    })
    .catch((err) => {
      const message = 'Error occurred creating device';

      console.log(message);

      res.status(500).json({message: message});
    });
});

/*app.get('/', function (req, res) {
  res.json({message: 'get / called'})
});*/

/*app.post('/', auth, function (req, res) {
  const name = req.body['name'];

  console.log(`request body name attribute: ${name}`);

  res.json({message: 'post / called'})
});*/

/*app.post('/bootstrap', auth, function (req, res) {
  User.create({email: 'a@b.com'})
    .then((user) => {
      console.log(`Created user: ${JSON.stringify(user)}`);

      Device.create({user: user._id, hostName: 'ali.local', ipAddress: '10.200.105.123'})
        .then((device) => {
          console.log(`Created device: ${JSON.stringify(device)}`);

          res.json(device);
        })
        .catch((err) => {
          console.log('Error occurred creating device');
        });
    })
    .catch((err) => {
      console.log('Error occurred creating device');
    });
});*/

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
