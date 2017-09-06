const server = require('./server');

server.start(function(port) {
    console.log('Server started on port ' + port);
});
