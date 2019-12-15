import flask
import shodan

# APIs
shodan_api = shodan.Shodan("bPeoBUXYuSxvw4YlP0j47yBzsPsaNiYt")

server = flask.Flask(__name__)


@server.route("/")
def home_page():
    # Random home page.
    return "Hello, World!"


@server.route("/check_proxy", methods = ["GET"])
def check_proxy():
    ip = flask.request.remote_addr
    print("IP:", ip)
    ip_info = shodan_api.host(ip)
    if "tags" in ip_info and "vpn" in ip_info["tags"] and "cloud" in ip_info["tags"]:
        return "ur on a proxy m8"
    else:
        return "ur not o a proxy"


@server.route("/check_fraud", methods = ["GET", "POST"])
def check_fraud():
    # Request body:
    #   "location"
    #   "time"
    #   "device-ip"
    #   "os-id"
    #   "browser-id"
    #   "device"
    #   "device-model"
    #   "sender-email"
    #   "recipient-email"
    #   "sender-id"
    #   "recipient-id"
    data = flask.request.json

    return data


server.run(debug = True, port = "42069")