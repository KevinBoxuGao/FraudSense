import flask
import torch
import torch.nn as nn
import shodan
import vincenty
import pickle
import block

# Exception class for server errors
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status = None, payload = None):
        self.message = message
        if status_code != None:
            status_code = status
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


# Get Model and Blockchain (ANONYMOUS FUNCTION IN classifier IS PLACEHOLDER)
block_chain = block.Chain()
classifier = lambda x: x

# APIs
shodan_api = shodan.Shodan("bPeoBUXYuSxvw4YlP0j47yBzsPsaNiYt")

# Flask server
server = flask.Flask(__name__)

@server.errorhandler(InvalidUsage)
def handle_error(error):
    response = flask.jsonify()
    response.status_code = error.status_code
    return response


@server.route("/")
def home_page():
    # Random home page.
    return "Hello, World!"


@server.route("/verify", methods = ["GET", "POST"])
def verify():
    # Request body:
    #   "amt"
    #   "location"
    #   "avg-location"
    #   "time"
    #   "device-ip"
    #   "os-id"
    #   "browser-id"
    #   "device"
    #   "device-model"
    #   "sender-email"
    #   "recipient-email"

    curr_transaction = flask.request.json
    last_transaction = block_chain.get_last_transaction(curr_transaction["sender-email"])

    # Check if IP is from a VPN (on cloud)
    ip_info = shodan_api.host(curr_transaction["device-ip"])
    on_proxy = 0
    if "tags" in ip_info and "cloud" in ip_info["tags"]:
        on_proxy = 1
    
    # Normalized to $100
    amount = curr_transaction["amt"] / 100

    # Normalized (from milliseconds) to days
    time_diff = (curr_transaction["time"] - prev_transaction["time"]) / 31536000000

    # Normalized to 1/2 of the Earth's circumference (in kilometres)
    distance = vincenty.vincenty(curr_transaction["location"], curr_transaction["avg-location"]) / 20000

    model_input = []
    output = classifier(model_input)

    if output[1] > 0.5:
        return flask.jsonify(genuine = False)
    elif output[0] > 0.5:
        # Verify block chain and delete fraudulent blocks.
        verified, fraudulent_idx = block_chain.verify()
        if not verified:
            block_chain.prune(fraudulent_idx)

        block_chain.add_block(curr_transaction)
        return flask.jsonify(genuine = True)
    else:
        raise InvalidUsage("Internal Server Error", 500)


server.run(host = "0.0.0.0", port = "5050")
