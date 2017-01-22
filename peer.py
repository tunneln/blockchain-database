from flask import Flask, render_template, request
from blockchain import Ledger
import click, requests, json, redis

app = Flask(__name__)

@click.command()
@click.option("--port", default=8000, help="Listening port.")
@click.option("--name", help="Peer name.")
@click.option("--peer-address", help="The URL of the peer to sync with.")
def start_peer(port, name, peer_address):
    start(name, peer_address)
    app.run(host="0.0.0.0", port=port, debug=False)


def start(name, peer_address):
    global peer_name
    global peers
    global redis_connection

    peer_name = name
    peers = [peer_address]
    redis_connection = redis.StrictRedis(host="localhost", port=6379, db=0)
    return app


def load_ledger():
    blockchain = read()
    ledger = Ledger()
    ledger.load_blockchain(blockchain)
    return ledger


@app.route("/")
def index():
    """
    Displays the state of the ledger.
    """
    ledger = load_ledger()
    return render_template("index.html",
                           ledger=ledger.values,
                           blockchain=ledger.blockchain,
                           name=peer_name)


@app.route("/ledger.json")
def ledger_json():
    """
    Display the block as a json document.
    """
    ledger = load_ledger()
    return json.dumps(ledger.values)


@app.route("/blockchain")
def blockchain():
    """
    Display the entire blockchain as an html file.
    """
    ledger = load_ledger()
    template = render_template("blockchain.html", blockchain=ledger.blockchain, name=peer_name)
    return template


@app.route("/invoke", methods=["POST"])
def invoke():
    """
    Kickstarts the network, adds adds a new, inital block,
    and responds to any peer requests to make a new block
    """
    ledger = load_ledger()
    key = request.form["key"]
    input_value = request.form["input"]
    block = ledger.update(key, input_value)
    write(ledger)
    try:
        if peers:
            send_peers("add_block", block.to_json())
    except Exception as excep:
        print str(excep)

    return str(block)


@app.route("/add_block", methods=["POST"])
def add_block():
    """
    Adds a block from another peer to the blockchain
    """
    ledger = load_ledger()
    json_block = json.loads(request.get_data())
    try:
        ledger.add_dict_block(json_block)
        write(ledger)
        return str(ledger.current_block)
    except Exception as e:
        return str(e)


def read():
    blockchain_json = redis_connection.get(peer_name)
    if blockchain_json is not None:
        return json.loads(blockchain_json)
    else:
        return []


def write(ledger):
    blockchain_json = ledger.blockchain_to_json()
    redis_connection.set(peer_name, blockchain_json)


def send_peers(endpoint, data):
    responses = []
    for peer in peers:
        try:
            url = "{}/{}".format(peer, endpoint)
            print url
            r = requests.post(url, data=data)
            responses.append(r)
        except Exception as e:
            print "Exception: Unable to post to peer {}: {}".format(str(e))
    return responses


if __name__ == "__main__":
    start_peer()
