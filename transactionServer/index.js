const http = require('http');
const Payment = require('./payment.js');
require('dotenv').config({path: __dirname + '/.env'});
const server = http.createServer(function(request, response) {
    console.dir(request.param);
    if (request.method == 'POST') { // Checks for POST request
        var body = '';
        request.on('data', function(data) {
            body += data; // Appends data if key-value pair to body
        });

        request.on('end', function() {
            body = JSON.parse(body);
            payment = new Payment(body.address1, body.address2);
            payment.pay();
            response.end('Transaction Successful');
        })
    } else if (request.method == 'GET') {
        var body = '';
        request.on('data', function(data) {
            body += data; // Appends data if key-value pair to body
        });

        request.on('end', function() {
            body = JSON.parse(body);
            process.env['SECRET'] = body.secret;
            response.end('Wallet creation successful');
        })
    }
});

const port = 3000;
server.listen(port);
console.log(`Listening on port ${port}`);