from flask import Flask, request, jsonify
import requests
from blockchain import Blockchain


# --------------------------
# NODE CLASS
# --------------------------
class Node:
    def __init__(self, port):
        """
        Each Node represents a participant in the blockchain network.
        Nodes can be Honest miners or Attackers.
        :param port: Port on which this node runs its Flask server.
        """
        self.app = Flask(__name__)  # Create a Flask web server
        self.blockchain = Blockchain()  # Each node has its own copy of blockchain
        self.peers = set()  # Store list of known peer nodes
        self.port = port  # Node's unique port number

        # --------------------------
        # API ROUTES
        # --------------------------

        @self.app.route('/new_transaction', methods=['POST'])
        def new_transaction():
            """
            Endpoint to receive a new transaction from user or peer node.
            """
            tx_data = request.get_json()
            required_fields = ["sender", "receiver", "amount"]

            # Ensure transaction has all required fields
            for field in required_fields:
                if not tx_data.get(field):
                    return "Invalid transaction data!", 400

            transaction = self.blockchain.add_transaction(
                tx_data['sender'], tx_data['receiver'], tx_data['amount']
            )

            # Broadcast transaction to peers
            self.broadcast_transaction(transaction)
            return "Transaction added successfully!", 201

        @self.app.route('/mine', methods=['GET'])
        def mine_block():
            """
            Endpoint for mining a new block.
            """
            miner_address = f"Node_{self.port}"  # Reward goes to this node
            new_block = self.blockchain.mine_pending_transactions(miner_address)

            # Broadcast mined block to peers
            self.broadcast_block(new_block)
            response = {
                "message": "Block mined successfully!",
                "index": new_block.index,
                "hash": new_block.hash,
                "transactions": new_block.transactions
            }
            return jsonify(response), 200

        @self.app.route('/chain', methods=['GET'])
        def get_chain():
            """
            Endpoint to return full blockchain of this node.
            """
            chain_data = [block.__dict__ for block in self.blockchain.chain]
            return jsonify(chain_data), 200

        @self.app.route('/add_block', methods=['POST'])
        def add_block():
            """
            Endpoint to accept a new block from a peer.
            """
            block_data = request.get_json()
            block = self.block_from_dict(block_data)

            # Verify block and add if valid
            if block.previous_hash == self.blockchain.get_last_block().hash:
                self.blockchain.chain.append(block)
                return "Block added successfully!", 201
            else:
                # If mismatch occurs, trigger chain resolution
                self.resolve_conflicts()
                return "Chain resolved", 200

        @self.app.route('/add_peer', methods=['POST'])
        def add_peer():
            """
            Endpoint to add a new peer node.
            """
            peer_data = request.get_json()
            peer_url = peer_data.get("peer")
            if peer_url:
                self.peers.add(peer_url)
                return f"Peer {peer_url} added successfully!", 201
            return "Invalid peer data", 400

    # --------------------------
    # HELPER FUNCTIONS
    # --------------------------

    def block_from_dict(self, block_data):
        """
        Convert block JSON data back into a Block object.
        """
        from blockchain import Block
        block = Block(
            index=block_data['index'],
            transactions=block_data['transactions'],
            previous_hash=block_data['previous_hash'],
            timestamp=block_data['timestamp'],
            nonce=block_data['nonce']
        )
        block.hash = block_data['hash']
        return block

    def broadcast_transaction(self, transaction):
        """
        Send transaction to all peers.
        """
        for peer in self.peers:
            url = f"{peer}/new_transaction"
            try:
                requests.post(url, json=transaction)
            except:
                pass  # Ignore unreachable peers

    def broadcast_block(self, block):
        """
        Send newly mined block to all peers.
        """
        block_data = block.__dict__
        for peer in self.peers:
            url = f"{peer}/add_block"
            try:
                requests.post(url, json=block_data)
            except:
                pass  # Ignore unreachable peers

    def resolve_conflicts(self):
        """
        Consensus algorithm:
        - Ask all peers for their chain
        - Adopt the longest valid chain
        """
        longest_chain = None
        current_len = len(self.blockchain.chain)

        for peer in self.peers:
            try:
                response = requests.get(f"{peer}/chain")
                peer_chain = response.json()
                if len(peer_chain) > current_len and self.validate_chain(peer_chain):
                    current_len = len(peer_chain)
                    longest_chain = peer_chain
            except:
                pass

        if longest_chain:
            # Replace local chain with longest valid peer chain
            from blockchain import Block
            self.blockchain.chain = [
                self.block_from_dict(b) for b in longest_chain
            ]

    def validate_chain(self, chain_data):
        """
        Validate a chain received from a peer.
        """
        from blockchain import Block
        chain = []
        for block_data in chain_data:
            block = self.block_from_dict(block_data)
            chain.append(block)

        # Use built-in validation
        self.blockchain.chain = chain
        return self.blockchain.is_chain_valid()

    def run(self):
        """
        Start the Flask server for this node.
        """
        self.app.run(port=self.port)


# --------------------------
# DEMO USAGE
# --------------------------
if __name__ == "__main__":
    # Example: Run a node on port 5000
    node = Node(5000)
    node.run()