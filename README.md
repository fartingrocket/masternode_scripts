# masternode_scripts
A script to do all the shitty job when there is a collateral change

* Compatible only with PIVX coins hosted on ihostmn.
* Requires python 3.6 or higher.
* Use at your own risk. No guarantees.

#Usage:

```python3 masternode_scripts.py [option1] [option2] [option3] ...```

#Examples:

```python3 masternode_scripts.py --checks```

```python3 masternode_scripts.py --delete --create```

#params.json file:

The file contains all the parameters needed to use the different functions
* ticker: SAPP, 777, UCR, etc...
* IHOSTMN-API-KEY: You need to get it from ihostmn so you can connect to your account 
  * visit https://ihostmn.com/settings.php to get your key.
* new_txs: the list of transaction hashes and transaction indexes to create new MNs. 
  Simply type in your wallet console `getmasternodeoutputs` and copy/paste the result

#Options:
```
        -h      --help          Get this menu.
        -c      --checks        Do checks on balance and existing masternodes
                                and offers the possibility to save masternode.conf file.
        -d      --delete        Delete all existing masternodes.
        -r      --create        Create new masternodes with transactions from params.json
                                and saves masternode.conf file automatically at the end.
        -i      --reindex       Reindex all existing masternodes wallets.
```