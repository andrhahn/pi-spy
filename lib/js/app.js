var spawn = require('child_process').spawn;

var child_process = spawn('ls', ['-al']);

child_process.stdout.on('data', function (data) {
    console.log('stdout: ' + data);
});

child_process.stderr.on('data', function (data) {
    console.log('grep stderr: ${data}');
});

child_process.on('close', function (code) {
    if (code !== 0) {
        console.log('grep process exited with code ${code}');
    }
});

// API methods
// start

module.exports = function(options) {
    // sdsfsdf

    return {

    };
};
