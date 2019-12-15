import flask
import torch
import torch.nn as nn
import shodan
import vincenty
import json
import block
from classifier import Classifier, one_hot_vectorize, os_identifier_map, browser_identifier_map, device_type_map, dev_info_map, email_map
from aggregate import interpret_browser_identifier, interpret_device_info, interpret_os_identifier

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
classifier = Classifier()
classifier.loadNet()

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


@server.route("/add-block", methods = ["POST"])
def add_block():
    data = flask.request.json
    block_chain.add_block(data)
    return "Block Added"


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

    with open("users.json", "r") as r:
        users = json.load(r)

        try:
            last_state = torch.Tensor(users[curr_transaction["sender-email"]])
        except KeyError:
            last_state = None
            users[curr_transaction["sender-email"]] = None
   
    # Check if IP is from a VPN (on cloud)
    on_proxy = 0
    try:
        ip_info = shodan_api.host(curr_transaction["device-ip"])
        if "tags" in ip_info and "cloud" in ip_info["tags"]:
            on_proxy = 1
    except:
        pass


    os = interpret_os_identifier(curr_transaction["os-id"])
    device_type = curr_transaction["device"]
    device_info = interpret_device_info(curr_transaction["device-model"])
    browser = interpret_browser_identifier(["browser-id"])
   
    # Normalized to $100
    amount = curr_transaction["amt"] / 100

    # Normalized (from milliseconds) to days
    time_diff = 1
    if last_transaction != None:
        time_diff = (curr_transaction["time"] - last_transaction.data["time"]) / 31536000000

    # Normalized to 1/2 of the Earth's circumference (in kilometres)
    distance = vincenty.vincenty(curr_transaction["location"], curr_transaction["avg-location"]) / 20000

    model_input = [amount, distance, time_diff, on_proxy] + \
                   one_hot_vectorize(os_identifier_map[os], 7) + \
                   one_hot_vectorize(browser_identifier_map[browser], 14) + \
                   one_hot_vectorize(device_type_map[device_type], 3) + \
                   one_hot_vectorize(dev_info_map[device_info], 23)
    print(amount, distance, time_diff, on_proxy)
                  
    output, state = classifier.forward(torch.Tensor([[model_input]]), last_state)
    users[curr_transaction["sender-email"]] = state.tolist()
    
    with open("users.json", "w") as w:
        json.dump(users, w)

    print(output)

    if output.view(-1)[1] < output.view(-1)[0] and output.view(-1)[0] > 0.5:
        # Verify block chain and delete fraudulent blocks.
        verified, fraudulent_idx = block_chain.verify()
        if not verified:
            block_chain.prune(fraudulent_idx)

        block_chain.add_block(curr_transaction)
        return flask.jsonify(genuine = True)
    else:
        return flask.jsonify(genuine = False)


server.run(host = "0.0.0.0", port = "5050", debug = True)
