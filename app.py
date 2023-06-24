from flask import Flask, jsonify, request
import requests
import os
import socket
import threading

app = Flask(__name__)

# Lista para almacenar los nodos conocidos
known_nodes = []
# Lista para almacenar los mensajes
messages = []

def get_container_ipv4_address():
    # Obtener el nombre de host del contenedor
    container_hostname = socket.gethostname()

    # Obtener la dirección IP del contenedor a partir del nombre de host
    container_ip = socket.gethostbyname(container_hostname)

    return container_ip

@app.route('/', methods=['GET'])
def hola():
    return jsonify({'message': 'Hola Mundo pulento'})

@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify(known_nodes)

@app.route('/messages', methods=['GET'])
def get_messages():
    last_n = request.args.get('last')
    if last_n is None:
        # If 'last' parameter is not provided, return all messages
        return jsonify(messages), 200
    else:
        # Ensure 'last' parameter is an integer before using it
        last_n = int(last_n)
        # Return the last 'n' messages
        return jsonify(messages[-last_n:]), 200


@app.route('/connect', methods=['POST'])
def connect_node():
    node = request.get_json()
    node_address = node.get('node_address')
    node_port = node.get('node_port')
    container_ipv4 = get_container_ipv4_address()

    try:
        response = requests.get(f'http://{node_address}:8080/nodes')
        node_list = response.json()

        for node in node_list:
            if node not in known_nodes:
                known_nodes.append(node)
                ip_nodo_vecino = node.split(':')[1].replace('//', '')
                requests.post(f'http://{ip_nodo_vecino}:8080/connect', json={'node_address': container_ipv4, 'node_port': os.getenv('MYPORT', '8080')})

        if (f'http://{node_address}:{node_port}') not in known_nodes:
            known_nodes.append(f'http://{node_address}:{node_port}')
            requests.post(f'http://{node_address}:8080/connect', json={'node_address': container_ipv4, 'node_port': os.getenv('MYPORT', '8080')})


    except requests.exceptions.ConnectionError:
        return 'Unable to connect', 400

    return jsonify(known_nodes), 200

@app.route('/messages', methods=['POST'])
def post_message():
    new_message = request.get_json()
    # Check if the message id already exists in the list
    existing_message = next((message for message in messages if (message['id'] == new_message['id'])), None)

    if existing_message:
        # If the message content and sender are the same, don't add or broadcast it
        if existing_message['message'] == new_message['message'] and existing_message['sender'] == new_message['sender']:
            return jsonify({'error': 'Message already exists'}), 409
        else:
            # If the id is the same but the message or sender are different, assign a new id
            new_message['id'] = max(message['id'] for message in messages) + 1
    
    messages.append(new_message)
    messages.sort(key=lambda x: (x['id'], x['sender']))
    # Broadcast the new message to all known nodes
    for node in known_nodes:
        node_address = node.split(':')[1].replace('//', '')
        requests.post(f'http://{node_address}:8080/messages', json=new_message)
    
    return jsonify(new_message), 201

def send_last_post():
    ip_nodo_vecino = os.getenv('IP', '')
    if ip_nodo_vecino != '':
        container_ipv4 = get_container_ipv4_address() 
        requests.post(f'http://{ip_nodo_vecino}:8080/connect', json={'node_address': container_ipv4, 'node_port': os.getenv('MYPORT', '8080')})
        print("Conectado al nodo vecino")


def runapp():
    container_ipv4 = get_container_ipv4_address()  # Obtiene la dirección IPv4 del contenedor
    self_node_url = f"http://{container_ipv4}:{os.getenv('MYPORT', '8080')}"
    known_nodes.append(self_node_url)
    app.run(host='0.0.0.0', port=8080, debug=False)



if __name__ == '__main__':
    first_thread = threading.Thread(target=runapp)
    second_thread = threading.Thread(target=send_last_post)
    first_thread.start()
    second_thread.start()
