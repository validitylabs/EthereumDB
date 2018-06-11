""" 
Author: Aleksandra Sokolowska
for Validity Labs AG
"""
def create_database(cur):
    """ create the schema for the database"""
    quick = """
    CREATE TABLE IF NOT EXISTS Quick (
     balanceFrom TEXT,
     balanceTo TEXT,
     blockNumber INTEGER, 
     sender TEXT,
     nonce INTEGER, 
     recipient TEXT,
     txHash TEXT PRIMARY KEY,
     value TEXT);"""

    tx = """
    CREATE TABLE IF NOT EXISTS TX (
     blockNumber INTEGER,
     contractAddress TEXT,
     cumulativeGasUsed INTEGER, 
     gas INTEGER, 
     gasPrice INTEGER, 
     gasUsed INTEGER,
     input TEXT, 
     logs TEXT, 
     logsBloom TEXT, 
     r TEXT, 
     s TEXT, 
     status INTEGER, 
     txHash TEXT PRIMARY KEY,
     transactionIndex INTEGER, 
     v INTEGER);"""

    blck = """
    CREATE TABLE IF NOT EXISTS block ( 
     blockGasUsed INTEGER, 
     blockHash TEXT, 
     blockLogsBloom TEXT, 
     blockNonce TEXT, 
     blockNumber INTEGER PRIMARY KEY, 
     difficulty TEXT, 
     extraData TEXT, 
     gasLimit INTEGER, 
     miner TEXT, 
     mixHash TEXT,      
     parentHash TEXT, 
     receiptsRoot TEXT, 
     sha3Uncles TEXT, 
     size INTEGER, 
     stateRoot TEXT, 
     timestamp INTEGER, 
     totalDifficulty TEXT, 
     transactions TEXT, 
     transactionsRoot TEXT, 
     uncles TEXT); """

    cur.execute(quick)
    cur.execute(blck)
    cur.execute(tx)

def create_index(cur):
    quick = "CREATE INDEX index_quick ON Quick(value, sender, recipient);"
    tx = "CREATE INDEX index_TX ON TX(blockNumber, status);"
    blck = "CREATE INDEX index_block ON block(timestamp);"
    
    cur.execute(quick)
    cur.execute(blck)
    cur.execute(tx)
    
def update_database(cur, table_quick, table_tx, table_block):
    """ write lists of dictionaries into the database"""
    quick = """INSERT INTO Quick VALUES (:balanceFrom, :balanceTo, :blockNumber, :from, :nonce, :to, :txHash, :value); """
    tx = """ INSERT INTO TX VALUES (:blockNumber, :contractAddress, :cumulativeGasUsed, :gas, :gasPrice, :gasUsed, :input, :logs, :logsBloom, :r, :s, :status, :txHash, :transactionIndex, :v); """
    blck = """ INSERT INTO block VALUES (:blockGasUsed, :blockHash, :blockLogsBloom, :blockNonce, :blockNumber,  :difficulty, :extraData, :gasLimit, :miner, :mixHash, :parentHash, :receiptsRoot, :sha3Uncles, :size, :stateRoot, :timestamp, :totalDifficulty, :transactions, :transactionsRoot, :uncles); """ 
    cur.executemany(quick, table_quick)
    cur.executemany(tx, table_tx)
    cur.executemany(blck, table_block)


