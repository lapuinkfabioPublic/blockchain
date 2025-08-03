from block import Blockchain
from flask import Flask, jsonify # type: ignore


app = Flask(__name__)
Blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = Blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = Blockchain.proof_of_work(previous_proof)
    previous_hash = Blockchain.hash(previous_block)
    block = Blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Parabéns, você minerou um bloco!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200