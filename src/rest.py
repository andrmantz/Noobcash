import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import json
from Crypto.Hash import SHA256

from block import Block
from node import Node
from transaction import Transaction
from txo import Txo
import socket
from threading import Lock

### JUST A BASIC EXAMPLE OF A REST API WITH FLASK


app = Flask(__name__)
CORS(app)
node: Node = None
block_requests = Lock()

# .......................................................................................

##### Network related and initializations


@app.route("/init_node", methods=["GET"])
def init_node():
    global node
    global port
    global is_bootstrap
    global mining_diffuculty
    global capacity

    node = Node(mining_difficulty, capacity, "localhost:" + str(port))
    # If i'm not bootstrap
    if is_bootstrap == 0:
        data = json.dumps(
            {
                "address": "localhost:" + str(port),
                "public_key": node.wallet.public_key,
            }
        )
        r = requests.post("http://localhost:5000/register", data=data)
        node.id = int(r.text)

    else:
        node.ring.add_node("localhost:5000", node.wallet.public_key)

    return "", 200


# Call on the bootstrap node when every client is connected to start the network
@app.route("/start", methods=["GET"])
def start_network():
    # We first create genesis block
    genesis = Block("1")
    genesis.nonce = 0
    genesis_transaction = Transaction(
        "0", 100 * len(node.ring.nodes), [], node.wallet.public_key
    )
    genesis_transaction.outputs = [
        Txo(genesis_transaction.id, node.wallet.public_key, 100 * len(node.ring.nodes))
    ]
    genesis.add_transaction(genesis_transaction)

    genesis.hash = genesis.myHash()
    node.ring.nodes[0].balance = genesis_transaction.amount
    node.wallet.add_transaction_to_wallet(genesis_transaction)

    node.blchain.add_block_to_chain(genesis)

    # We first share the ring and chain to all nodes

    addresses = node.ring.get_addresses(node.wallet.public_key)
    ringnodes = []
    for n in node.ring.nodes:
        ringnodes.append(n.todict())

    data = pickle.dumps([node.blchain.chain, ringnodes])
    for addr in addresses:
        r = requests.post(f"http://{addr}/init_data", data=data)
        while not r.ok:
            r = requests.post(f"http://{addr}/init_data", data=data)

    # Then we send 100 NBC to each node
    for n in node.ring.nodes:
        if n.id == 0:
            continue
        node.create_transaction(n.public_key, 100)

    return "", 200


@app.route("/register", methods=["POST"])
def register():
    data = json.loads(request.data)
    id = node.ring.add_node(data["address"], data["public_key"])
    print(f"Just accepted node with id {id}")
    return f"{id}", 200


@app.route("/init_data", methods=["POST"])
def init_data():
    # data = [chain, ring]
    data = pickle.loads(request.get_data())
    node.blchain.chain = data[0]

    # Init RingNodeList
    ring_json = data[1]
    for i in ring_json:
        node.ring.add_node(
            i["address"], i["public_key"], id=i["id"], balance=i["balance"]
        )

    node.ring.nodes.sort(key=lambda x: x.id)

    print(f"I'm node {node.id} and i am ready to start")
    return "", 200


@app.route("/whoami", methods=["GET"])
def whoami():
    return f"Hi, I am node {node.id}", 200


@app.route("/dump_chain", methods=["GET"])
def lala():
    return f"{node.blchain.dumpit()}"


@app.route("/block", methods=["GET"])
def lolo():
    return f"{node.current_block.tostr(node.ring)}"


#### Broadcast endpoints
@app.route("/new_block", methods=["POST"])
def new_block():
    with block_requests:
        bl = pickle.loads(request.get_data())
        node.accept_block(bl)
    return ""


@app.route("/new_transaction", methods=["POST"])
def new_transaction():
    with block_requests:
        tr = pickle.loads(request.get_data())
        node.accept_transaction(tr)

    return ""


@app.route("/start_consensus", methods=["GET"])
def start_consensus():
    with block_requests:
        # if len(node.blchain.chain) - 1 == node.blchain.checkpoint:
        #     return "", 400
        node.resolve_conflicts()
    return "", 200


@app.route("/chain", methods=["GET"])
def send_chain():
    # pickled_chain = pickle.dumps(node.blchain.get_from_checkpoint())
    pickled_chain = pickle.dumps(node.blchain.chain)
    return pickled_chain, 200


#### Miner endpoint
@app.route("/mined", methods=["POST"])
def mined():
    with block_requests:
        node.stop_mine()
        node.miner.clear_miner()
        mined_block = pickle.loads(request.get_data())
        if node.valid_block(mined_block, node.blchain.last_block()):
            node.blchain.add_block_to_chain(mined_block)
            node.broadcast_block()
            node.create_new_block()
            node.trigger_queue()
            node.check_mine()

    return "ok", 200


@app.route("/wq", methods=["GET"])
def pepe():
    wq = node.uncommited_transactions()
    for i in wq:
        print(i.tostr(node.ring))
    if not node.current_block:
        print("No current block")
    else:
        print(len(node.current_block.listOfTransactions))
    return ""


@app.route("/stat", methods=["GET"])
def ooo():
    if node.miner.running():
        print("trying")
    else:
        print("I dont care about ya")
    return ""


#### Client endpoints
@app.route("/create_transaction", methods=["POST"])
def create_transaction():
    with block_requests:
        try:
            data = json.loads(request.data)
            id = int(data["id"])
            amount = int(data["amount"])

            address = node.ring.nodes[id].public_key
            t = node.create_transaction(address, amount)

        except Exception as e:
            print(e)
            return jsonify(f"{e}\n"), 403

    return jsonify("Transaction accepted!\n"), 200


@app.route("/nodes", methods=["GET"])
def get_nodes():
    data = [
        {
            "id": n.id,
            "label": n.public_key,
            "public_key": n.public_key,
            "address": n.address,
            "balance": n.balance,
        }
        for n in node.ring.nodes
    ]
    return jsonify(data), 200


@app.route("/incomes", methods=["GET"])
def incomes():
    if len(node.blchain.chain) == 0:
        return jsonify([]), 200

    transactions = node.wallet.transactions
    data = []
    for transaction in transactions:
        if transaction.receiver_address == node.wallet.public_key:
            data.append(
                {
                    "sender_index": node.ring.get_id_by_public_key(
                        transaction.sender_address
                    ),
                    "sender_address": transaction.sender_address,
                    "amount": transaction.amount,
                    "index": transaction.id,
                }
            )
    return jsonify(data), 200


@app.route("/outcomes", methods=["GET"])
def outcomes():
    if len(node.blchain.chain) == 0:
        return jsonify([]), 200

    transactions = node.wallet.transactions
    data = []
    for transaction in transactions:
        if transaction.sender_address == node.wallet.public_key:
            data.append(
                {
                    "receiver_index": node.ring.get_id_by_public_key(
                        transaction.receiver_address
                    ),
                    "receiver_address": transaction.receiver_address,
                    "amount": transaction.amount,
                    "index": transaction.id,
                }
            )
    return jsonify(data), 200


@app.route("/transactions", methods=["GET"])
def transactions():
    if len(node.blchain.chain) == 0:
        return jsonify([]), 200

    transactions = node.wallet.transactions
    data = []
    for transaction in transactions:
        data.append(
            {
                "sender_index": node.ring.get_id_by_public_key(
                    transaction.sender_address
                ),
                "sender_address": transaction.sender_address,
                "receiver_index": node.ring.get_id_by_public_key(
                    transaction.receiver_address
                ),
                "receiver_address": transaction.receiver_address,
                "amount": transaction.amount,
                "index": transaction.id,
            }
        )
    return jsonify(data), 200


@app.route("/profile", methods=["GET"])
def profile():
    return {
        "id": node.id,
        "public_key": node.wallet.public_key,
    }, 200


@app.route("/balance", methods=["GET"])
def balance():
    return f"{node.wallet.balance()}", 200


@app.route("/last_block", methods=["GET"])
def last_block_transactions():
    if len(node.blchain.chain) == 0:
        return jsonify([]), 200

    transactions = node.blchain.last_block().listOfTransactions

    data = []
    for transaction in transactions:
        data.append(
            {
                "sender_index": node.ring.get_id_by_public_key(
                    transaction.sender_address
                ),
                "sender_address": transaction.sender_address,
                "receiver_index": node.ring.get_id_by_public_key(
                    transaction.receiver_address
                ),
                "receiver_address": transaction.receiver_address,
                "amount": transaction.amount,
                "index": transaction.id,
            }
        )
    return jsonify(data), 200


#### Tests
@app.route("/test", methods=["GET"])
def testit():
    i = 0
    with open(
        "/home/andreas/Documents/uni/noobcash/Testing/5nodes/transactions"
        + str(node.id)
        + ".txt",
        "r",
    ) as f:
        for line in f:
            _, id, amount = line.split(" ")
            id = int(id)
            amount = int(amount)
            address = node.ring.nodes[id].public_key
            t = node.create_transaction(address, amount)
    return "ok"


@app.route("/cons", methods=["GET"])
def cons():
    node.request_consensus()
    return "ok"


# run it once fore every node

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    parser.add_argument("--bootstrap", default=0, type=int)
    parser.add_argument("--difficulty", default=5, type=int)
    parser.add_argument("--capacity", default=5, type=int)
    args = parser.parse_args()
    port = args.port
    is_bootstrap = args.bootstrap
    mining_difficulty = args.difficulty
    capacity = args.capacity

    app.run(host="127.0.0.1", port=port, threaded=True)
