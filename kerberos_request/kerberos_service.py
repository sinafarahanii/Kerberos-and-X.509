from flask import Flask, request, jsonify
import hashlib
import random

app = Flask(__name__)


# KDC (Key Distribution Center)

class KDC:
    def __init__(self):
        self.secret_key = "secret-key"
        self.database = {} 

    def register_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.database[username] = hashed_password

    def authenticate(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username in self.database and self.database[username] == hashed_password:
            return True
        return False

    def generate_ticket(self, username):
        session_key = hashlib.sha256(str(random.random()).encode()).hexdigest()
        ticket = f"TICKET_{username}_{session_key}"
        return ticket, session_key

# TGS (Ticket Granting Server)


class TGS:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def verify_ticket(self, ticket):
        return ticket.startswith("TICKET_")

    def issue_service_ticket(self, service_name, session_key):
        service_session_key = hashlib.sha256((service_name + session_key).encode()).hexdigest()
        service_ticket = f"SERVICE_TICKET_{service_name}_{service_session_key}"
        return service_ticket

"""
    Service class for verifying service tickets.

    Methods:
        verify_service_ticket(service_ticket):
            Verifies if the provided service ticket is valid by checking if it starts with the service's name.
"""
class Service:
    def __init__(self, name):
        self.name = name

    def verify_service_ticket(self, service_ticket):
        return service_ticket.startswith(f"SERVICE_TICKET_{self.name}_")


# Initialize KDC, TGS, and Service instances
kdc = KDC()
tgs = TGS(kdc.secret_key)
service = Service("example_service")


@app.route('/register', methods=['POST'])
def register_user():
    """
    Registers a new user with the KDC (Key Distribution Center).
    
    Expects a JSON request body containing the username and password. The password is hashed and stored in the KDC's database.

    Returns a success message if the user is registered successfully.
    """
    data = request.json
    print(data)
    username = data.get('username')
    password = data.get('password')
    kdc.register_user(username, password)
    return jsonify({"message": f"User {username} registered successfully"}), 200


@app.route('/authenticate', methods=['GET'])
def authenticate():
    """
    Authenticates a user by checking their username and password with the KDC.
    
    Expects a JSON request body containing the username and password. If authenticated, a ticket and session key are generated and returned.
    
    Returns a success message with the ticket and session key if authentication is successful, otherwise returns an authentication failure message.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if kdc.authenticate(username, password):
        ticket, session_key = kdc.generate_ticket(username)
        return jsonify({"ticket": ticket, "session_key": session_key}), 200
    else:
        return jsonify({"message": "Authentication failed"}), 401


@app.route('/verify_ticket', methods=['GET'])
def verify_ticket():
    """
    Verifies the validity of a provided ticket with the TGS (Ticket Granting Service).
    
    Expects a JSON request body containing the ticket.
    
    Returns a success message if the ticket is valid, otherwise returns an invalid ticket message.
    """
    data = request.json
    ticket = data.get('ticket')
    if tgs.verify_ticket(ticket):
        return jsonify({"message": "Ticket verified"}), 200
    else:
        return jsonify({"message": "Invalid ticket"}), 400


@app.route('/issue_service_ticket', methods=['GET'])
def issue_service_ticket():
    """
    Issues a service ticket for a specific service by combining the service name and session key.
    
    Expects a JSON request body containing the service name and session key. Returns the generated service ticket if successful.
    """
    data = request.json
    service_name = data.get('service_name')
    session_key = data.get('session_key')
    service_ticket = tgs.issue_service_ticket(service_name, session_key)
    return jsonify({"service_ticket": service_ticket}), 200


@app.route('/verify_service_ticket', methods=['GET'])
def verify_service_ticket():
    """
    Verifies the validity of a provided service ticket.
    
    Expects a JSON request body containing the service ticket.
    
    Returns a success message if the service ticket is valid, otherwise returns an invalid service ticket message.
    """
    data = request.json
    service_ticket = data.get('service_ticket')
    if service.verify_service_ticket(service_ticket):
        return jsonify({"message": "Service ticket verified"}), 200
    else:
        return jsonify({"message": "Invalid service ticket"}), 400


if __name__ == '__main__':
    app.run(debug=False)