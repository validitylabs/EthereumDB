# EthereumDB (Python and SQL)

Create the EthereumDB containing data residing on the Ethereum blockchain. 
Database management system: SQLite.

## Create a database
1. Connect to [Infura](https://www.infura.io) (or run a local node).
2. Uncomment and specify the path in ```database.py```:

```python
#uncomment one of the options below
# 1. connection via Infura
#web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/your-personal-number"))

# 2. or connection via local node 
#web3 = Web3(Web3.IPCProvider('/your-path-to/geth.ipc'))
```
3. execute:
```python database.py```


## More on database design

Database consists of 3 tables:
- **Quick**: most relevant transaction info for quick access & analysis
- **TX**: all remainder transaction info
- **Block**: block-specific info

Quick | TX | Block
------|----|------
'from'/'sender', 'to'/'recipient', 'value', 'nonce', 'blockNumber', 'txHash', 'balanceTo', 'balanceFrom' | 'blockNumber', 'gas', 'gasPrice', 'input', 'transactionIndex', 'v', 'r', 's', 'contractAddress', 'cumulativeGasUsed', 'gasUsed', 'logs', 'logsBloom', 'status', 'transactionHash' | 'difficulty', 'extraData', 'gasLimit', 'blockGasUsed', 'blockHash', 'blockLogsBloom', 'miner', 'mixHash', 'blockNonce', 'blockNumber', 'parentHash', 'receiptsRoot', 'sha3Uncles', 'size', 'stateRoot', 'timestamp', 'totalDifficulty', 'transactions', 'transactionsRoot', 'uncles'

### Meaning of the variables in the EthereumDB

#### Quick
Variable | Meaning
--- | --- 
**sender** | 160-bit address of a sender of a transaction
**recipient** | address of the recipient or null for a contract creation transaction
**value** | number of wei to be transfered to the recipient or newly created account (case of contract creation)
**nonce** | number of transactions/contract creations sent by the sender prior to this one
**blockNumber** | number of the block the transaction belongs to (PRIMARY KEY)
**txHash** | transaction hash (unique identifier)
**balanceTo** | balance of the recipient **after that transaction** (note: different than balance from web3 which is after all tx-s in the block)
**balanceFrom** | balance of the sender **after that particular transaction** (note: different than balance from web3 which is after all tx-s in the block)

#### TX
Variable | Meaning
--- | --- 
**blockNumber** | number of the block the transaction belongs to
**gas**| gas consumed by the transaction
**gasPrice** | number of Wei to be paid per unit of gas for all computatioon costs of this transaction
**input** | the data sent along with the transaction
**transactionIndex** | index of the transaction in the block
**v, r, s** | used to identify the sender; the signature values of the transaction
**contractAddress** | the contract address created, if the transaction was a contract creation, otherwise null
**cumulativeGasUsed** | the sum of **gasUsed** by this transaction and all preceding transactions in the same block
**gasUsed** | the total amount of gas used when this transaction was executed in the block
**logs** | array of log objects, which the transaction has generated
**logsBloom** | the Bloom filter from indexable info (logger address and log topics) contained in each log entry from the receipt of each transaction in the transaction list
**status** | boolean whether the transaction was successfull; false if the EVM (Ethereum Virtual Machine) reverted the transaction
**txHash** | transaction hash (unique identifier) (PRIMARY KEY)

#### Block
Variable | Meaning
--- | --- 
**difficulty** | scalar value corresponding to the difficulty level of the block
**extraData** | extra data in byte array
**gasLimit** | maximum gas expenditure allowed in this block
**blockGasUsed** | total gas used by all transactions in this block 
**blockHash** | hash of the block 
**blockLogsBloom** | the Bloom filter from indexable info (logger address and log topics) 
**miner** |  160-bit address for fees collected from successful mining
**mixHash** | 256-bit hash, which is combined with the nonce and used to prove that sufficient amount of computation has been carried out on this block
**blockNonce** | hash of the generated proof-of-work; null when its a pending block
**blockNumber** | scalar value equal to the number of ancestor blocks (genesis block=0)
**parentHash** | Keccak256 hash of the parent block's header
**receiptsRoot** | Keccak 256-bit hash of the root node of the tree structure populated with receipts of all transactions in this block
**sha3Uncles** | SHA3 of the uncles data in the block.
**size** | size of the block in bytes
**stateRoot** | Keccak256 hash of the root node if the state trie, after all transactions are executed and finalisations applied
**timestamp** | Unix's time() at this block's inception 
**totalDifficulty** | integer of the total difficulty of the chain until this block 
**transactions** | list of transaction hashes included in the block
**transactionsRoot** | Keccak256 hash of the root node of the trie structure populated with the receipts of each transaction in the transactions list
**uncles** | list of uncle hashes



[source1](https://ethereum.github.io/yellowpaper/paper.pdf)
[source 2](https://ethereum.stackexchange.com/questions/10548/what-does-every-field-in-block-means)
[source 3](https://github.com/4c656554/BlockchainIllustrations/blob/master/Ethereum/EthBlockchain5.svg)
[source 4](https://web3js.readthedocs.io/en/1.0/web3-eth.html#gettransaction)
[source5](https://web3js.readthedocs.io/en/1.0/web3-eth.html#gettransactionreceipt)

## How to use the database

```python
import sqlite3 as sq3
conn = sq3.connect("blockchain.db")
cur = conn.cursor()

# some SQL code, e.g. select first five entries of the table Quick
cur.execute("SELECT * FROM Quick LIMIT 5")
a = cur.fetchall() #list of tuples containing all elements of the row
print(a)
conn.close()
```

###### Warning: the full database is large. You might not be able to open everything in one go.
