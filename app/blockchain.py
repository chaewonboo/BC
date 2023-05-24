import time
import hashlib
import json
from uuid import uuid4
from urllib.request import urlopen
import requests

class Blockchain:
    def __init__(self, current_node_url=None):
        self.chain = []
        self.pending_transactions = []
        self.current_node_url = current_node_url
        self.network_nodes = []
        self.create_genesis_block()
        
        

    def create_new_block(self, nonce, previous_block_hash, hash_, merkle_root):
        new_block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time.time() * 1000),
            'transactions': self.pending_transactions,
            'merkel_tree_process' : self.merkle_tree_proecss,
            'merkle_root': merkle_root,
            'nonce': nonce,
            'hash': hash_,
            'previous_block_hash': previous_block_hash
        }
        self.pending_transactions = self.create_new_transaction(6.25,'00',self.node_address())
        self.chain.append(new_block)
        return new_block
    
    def get_last_block(self):
        return self.chain[len(self.chain) - 1]
    
    def create_new_transaction(self,amount,sender,recipient):
        new_transaction = {
            'amount' : amount,
            'sender' : sender,
            'recipient' : recipient,
            'transaction_id': str(uuid4()).replace('-', '')
        }
        return new_transaction

    def hash_block(self, previous_block_hash, current_block_data, nonce):
        data_as_string = previous_block_hash + str(nonce) + json.dumps(current_block_data, separators=(',', ':'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        hash_object = hashlib.sha256(data_as_string.encode())
        hash_ = hash_object.hexdigest()
        return hash_
    
    def proof_of_work(self,previous_block_hash, current_block_data):
        nonce = 0
        hash_ = self.hash_block(previous_block_hash, current_block_data, nonce)
        while hash_[:4] != '0000':
            nonce += 1
            hash_ = self.hash_block(previous_block_hash, current_block_data, nonce)
            print(hash_)
        return nonce
    
    def add_transaction_to_pending_transactions(self,transaction_obj):
        self.pending_transactions.append(transaction_obj)
        return self.get_last_block()['index'] + 1
    
    def add_genesis_transaction(self,transaction_obj):
        self.pending_transactions.append(transaction_obj)
        return True

    def chain_is_valid(self, chain):
        genesis_block = chain[0]
        #proof_of_work함수 써서 nonce값이 맞는지 검증
        #self.proof_of_work(genesis_block['previous_block_hash'], genesis_block['merkle_root']{})
        correct_nonce = genesis_block['nonce'] == self.proof_of_work(genesis_block['previous_block_hash'], {'merkle_root': genesis_block['merkle_root'], 'index': 1})
        correct_previous_block_hash = genesis_block['previous_block_hash'] == self.hash_function('0') #genesis block의 hash값은 "0" hash한것
        #hash_block함수 써서 hash값 맞는지 검증
        correct_hash = genesis_block['hash'] == self.hash_block(genesis_block['previous_block_hash'], {'merkle_root': genesis_block['merkle_root']}, genesis_block['nonce']) 
        correct_transactions = len(genesis_block['transactions']) == 1 #genesis block의 tx의 길이는 1(coinbase tx)
        validChain  = True

        if not (correct_nonce and correct_previous_block_hash and correct_hash and correct_transactions):
            validChain = False

        for i in range(1, len(chain)):
            current_block = chain[i]
            prev_block = chain[i - 1]

            block_hash = self.hash_block(prev_block['hash'],{"merkle_root": current_block['merkle_root'], "index": current_block['index']}, current_block['nonce'])
            print(block_hash)
            #채우시오 hash 값 앞 4자리가 0이 아니면 false:
            if block_hash[:4]!= '0000':
                validChain = False
            #채우시오 이전 block의 hash값은 현재 블럭의 previous_block_hash랑 같아야함:
            if prev_block['block_hash']!= current_block['previous_block_hash']:
                validChain = False

        return validChain
    
    def get_block(self, block_hash):
        correct_block = None
        for block in self.chain:
            if block['hash'] == block_hash:
                correct_block = block
                break
        return correct_block

    def get_transaction(self, transaction_id):
        correct_transaction = None
        correct_block = None
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['transaction_id'] == transaction_id:
                    correct_transaction = transaction
                    correct_block = block
                    break
            if correct_transaction:
                break
        return {
            'transaction': correct_transaction,
            'block': correct_block
        }

    def get_address_data(self, address):
        address_transactions = []
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['sender'] == address or transaction['recipient'] == address:
                    address_transactions.append(transaction)

        balance = 0
        for transaction in address_transactions:
            if transaction['recipient'] == address:
                balance += transaction['amount']
            elif transaction['sender'] == address:
                balance -= transaction['amount']

        return {
            'addressTransactions': address_transactions,
            'addressBalance': balance
        }
    
    def hash_function(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def create_merkle_tree_node(self, left, right):
        self.merkle_tree_proecss.append(self.hash_function(left))
        self.merkle_tree_proecss.append(self.hash_function(right))
        self.merkle_tree_proecss.append(self.hash_function(left + right))
        return self.hash_function(left + right)
    
    def create_merkle_tree(self, transactions):
        if len(transactions) == 0:
            print("1")
            return None


        elif len(transactions) == 1: # 제네시스 및 처음부터 한개일때
            transactions.append(transactions[-1])
            new_level = []
            for i in range(0, len(transactions), 2):
                left = transactions[i]
                right = transactions[i + 1]
                new_level.append(self.create_merkle_tree_node(left, right))
            
            transactions = new_level

            return transactions[0]
        
        else: #두개
            while len(transactions) > 1:
                if len(transactions) % 2 != 0:
                    transactions.append(transactions[-1])

                new_level = []
                for i in range(0, len(transactions), 2):
                    left = transactions[i]
                    right = transactions[i + 1]
                    new_level.append(self.create_merkle_tree_node(left, right))

                transactions = new_level

            return transactions[0]
    
    def node_address(self):
        node_address = str(uuid4()).replace('-', '')
        return node_address
    
    def create_genesis_block(self):
        self.merkle_tree_proecss = []
        self.add_genesis_transaction({'amount' : 50,'sender': '0','recipient':self.node_address(),'transaction_id' : str(uuid4()).replace('-','')})
        self.genesis_merkleroot = self.create_merkle_tree([self.hash_function(str(tx)) for tx in self.pending_transactions])
        self.genesis_nonce = self.proof_of_work(self.hash_function('0'), {'merkle_root':self.genesis_merkleroot,'index' : 1})
        self.create_new_block(self.genesis_nonce, self.hash_function('0'), self.hash_block(self.hash_function('0'), {'merkle_root':self.genesis_merkleroot,'index' : 1},self.genesis_nonce), self.genesis_merkleroot)
    