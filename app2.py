#Fabio Leandro Lapuinka
from block import JadeBlockchain
from flask import Flask, jsonify # type: ignore
from uuid import uuid4


app = Flask(__name__)

node_address = str(uuid4()).replace('-', '')

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
Blockchain = JadeBlockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = Blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = Blockchain.proof_of_work(previous_proof)
    previous_hash = Blockchain.hash(previous_block)
    Blockchain.add_transaction(sender=node_address, receiver='Fabio', amount=1)
    block = Blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Parabéns, você minerou um bloco!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions']
    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': Blockchain.chain,
        'length': len(Blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = Blockchain.is_chain_valid(Blockchain.chain)
    if is_valid:
        response = {'message': 'Tudo certo. O blockchain é válido.'}
    else:
        response = {'message': 'O blockchain não é válido.'}
    return jsonify(response), 200

app.run(host='0.0.0.0', port=5000)  
