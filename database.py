""" 
Author: Aleksandra Sokolowska
for Validity Labs AG
"""

from web3 import Web3
from organize import *
import time

#uncomment one of the options below
# 1. connection via Infura
#web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/your-personal-number"))

# 2. or connection via local node 
#web3 = Web3(Web3.IPCProvider('/your-path-to/geth.ipc'))

# load a block.
Nblocks = 10000
output_every = 2
start_time = time.time()
try:
    with open('lastblock.txt', 'r') as f:
        start = int(f.read())+1
except FileNotFoundError:
    start = 2000000

#define tables that will go to the SQLite database
table_quick = []
table_tx = []
table_block = []

count = 0
#loop over all blocks
for block in range(start, start+Nblocks):
    
    block_table, block_data = order_table_block(block,web3)
    #list of block data that will go to the DB
    table_block.append(block_table)

    #all transactions on the block
    for hashh in block_data['transactions']:
        #print(web3.toHex(hashh))       
        quick_table, tx_data = order_table_quick(hashh,block, web3)
        table_quick.append(quick_table)
        
        #list of tx data that will go to the DB
        TX_table = order_table_tx(tx_data,hashh, web3)
        table_tx.append(TX_table)
    count = count + 1
    #print(count)
    #dump output every 2 blocks
    if (count % output_every) == 0:
        execute_sql(table_quick, table_tx, table_block)
        
        #free up memory
        del table_quick
        del table_tx
        del table_block
        table_quick = []
        table_tx = []
        table_block = []
        
        #update the current block number to a file
        with open('lastblock.txt', 'w') as f:
            f.write("%d" % block)
    if (count % 10) == 0:
        end = time.time()
        with open('timeperXblocks.txt', 'a') as f:
            f.write("%d %f \n" % (block, end-start_time))
    if (count % 100) == 0:
        print("100 new blocks completed.")