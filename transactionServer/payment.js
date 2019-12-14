require('dotenv').config({path: __dirname + '/.env'});
const RippleAPI = require('ripple-lib').RippleAPI;

class Payment {
    constructor(address1, address2) {
        this.a1 = address1;
        this.a2 = address2;
        this.api = new RippleAPI({
            //server: 'wss://s1.ripple.com'                 // MAINNET
            server: 'wss://s.altnet.rippletest.net:51233'   // TESTNET
        });
        this.instructions = {maxLedgerVersionOffset: 5}
        this.currency = 'XRP'
        this.amount = '10.00'

        this.payment = {
            source: {
                address: this.a1,
                maxAmount: {
                value: this.amount,
                currency: this.currency
                }
            },
            destination: {
                address: this.a2,
                amount: {
                value: this.amount,
                currency: this.currency
                }
            }
        }

    }

    pay(amount) {
        this.api.connect().then(() => {
            console.log("connected")
            this.api.preparePayment(this.a1, this.payment, this.instructions).then(prepared => {
        
                const {signedTransaction, id} = this.api.sign(prepared.txJSON, process.env['SECRET'])
                console.log(id)
                this.api.submit(signedTransaction).then(result => {
                  console.log(JSON.stringify(result, null, 2))
                  this.api.disconnect()
                });
            });
        }).catch(console.error)
    }
}

module.exports = Payment;