# masternode_scripts
A script to do all the shitty job when there is a collateral change

* Compatible only with non dip coins hosted on ihostmn.
* Requires python 3.6 or higher.
* Use at your own risk. No guarantees.

# Usage:

```python3 masternode_scripts.py [option]```

only one option at a time is allowed

# Examples:

```python3 masternode_scripts.py --checks```

Will yield the following result (obviously all the info is fake, don't try to search it)

```
#### Account Balance ####################################

  Current balance = 2.16 EUR

#### List all Masternodes ###############################

Masternode MN1-XXXXX : ticker 777
  tx id    : o3xs3e02cxxvbp0ujzv5e47nlk0la6ju97dtujvoov20kekmnqh2zvsaimnztcok
  tx index : 0

Masternode MN2-XXXXX : ticker 777
  tx id    : sufx1i6rp27neypitm8b2qcykshayxqw1v44vfe5yo1ekx3ciasn7jo0feanjyv3
  tx index : 0

Masternode MN3-XXXXX : ticker 777
  tx id    : khro35p0ycdo5m41d29p4cauui2wwqwoa050klhtznmf8o3gcvobw0cr3t0oz1f1
  tx index : 1

#### Save masternode.conf ##############################

Do you want to save masternode.conf file ? (y/n) : y
masternode.conf saved to ~/Documents/masternode_scripts
```

# params.json file:

The file contains all the parameters needed to use the different functions
* ticker: SAPP, 777, UCR, etc...
* alias_prefix: prefix for naming the newly created masternodes (default = "MN", so by default the created masternodes 
  will have aliases: MN1, MN2, etc...)
* IHOSTMN-API-KEY: You need to get it from ihostmn so you can connect to your account 
  * visit https://ihostmn.com/settings.php to get your key.
* new_txs: the list of transaction hashes and transaction indexes to create new MNs. 
  Simply type in your wallet console `getmasternodeoutputs` and copy/paste the result

# Options:

```
        -h      --help          Get this menu.
        -c      --checks        Do checks on balance and existing masternodes
                                and offers the possibility to save masternode.conf file.
        -d      --delete        Delete all existing masternodes.
        -r      --create        Create new masternodes with transactions from params.json
                                and saves masternode.conf file automatically at the end.
        -r      --delcreate     Delete old masternodes and create new ones with transactions from params.json
                                then save masternode.conf file automatically at the end.
        -i      --reindex       Reindex all existing masternodes wallets.
```