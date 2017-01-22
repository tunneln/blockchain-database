from flask import Flask, render_template, request, redirect
import click, client, requests

app = Flask(__name__)


@click.command()
@click.option("--port", default=8080, help="Listening port.")
@click.option("--name")
@click.option("--peer-address", default="http://127.0.0.1:8000")
def run(port, name, peer_address):
    start(name, peer_address)
    app.run(host="0.0.0.0", port=port, debug=False)


def start(name, peer_address):
    global s_name
    global peer

    s_name = name
    peer = peer_address
    return app


@app.context_processor
def inject_context():
    return dict(site=s_name, peer=peer)


@app.route("/")
def index():
    ledger = client.get_ledger(peer)
    return render_template("index.html", ledger=ledger)


@app.route("/file", methods=["POST"])
def post_file():
    acid = request.form.get("ACID")
    client.invoke(peer, acid, "FILED")
    return redirect("/", code=302)


@app.route("/close", methods=["POST"])
def close():
    acid = request.form.get("ACID")
    state = "CLOSED"
    client.invoke(peer, acid, state)
    return redirect("/", code=302)


@app.route("/open", methods=["POST"])
def open():
    acid = request.form.get("ACID")
    state = "ACTIVE"
    client.invoke(peer, acid, state)
    return redirect("/", code=302)


def get_ledger(peer_address):
    url = "{}/{}".format(peer_address, "ledger.json")
    r = requests.get(url)
    return r.json()


def invoke(peer_address, key, input_value):
    url = "{}/{}".format(peer_address, "invoke")
    val = {
        "key": key,
        "input": input_value,
        }
    ret = requests.post(url, data=val)
    return ret


if __name__ == "__main__":
    run()
