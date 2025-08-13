#Fabio Leandro Lapuinka
from  jadecoin import JadeBlockchain
from flask import Flask, jsonify # type: ignore
from uuid import uuid4
from flask import request


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
    Blockchain.add_transaction(sender=node_address, receiver='Fabio5003', amount=1)
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

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Algumas chaves estão faltando', 400
    index = Blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'A transação será adicionada ao bloco {index}'}
    return jsonify(response), 2010

@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'Nenhum nó', 400
    for node in nodes:
        Blockchain.add_node(node)
    response = {
        'message': 'Todos os nós foram conectados. O blockchain contém agora os seguintes nós:',
        'total_nodes': list(Blockchain.nodes)
    }
    return jsonify(response), 201

@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = Blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Os nós tinham cadeias diferentes. Foram substituídas pela mais longa.',
                    'new_chain': Blockchain.chain}
    else:
        response = {'message': 'Todos os nós já tinham a cadeia mais longa.',
                    'actual_chain': Blockchain.chain}
    return jsonify(response), 200

app.run(host='0.0.0.0', port=5003)  

