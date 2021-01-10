# General description:
masternode_scripts is script to do all the shitty job when there is a collateral change

* Compatible only with non dip coins hosted on ihostmn.
* Requires python 3.6 or higher.
* Use at your own risk. No guarantees.

# Options:

```
  -h      --help          Get this menu.

  -g      --configure     Starts the configuration manager
                          helps creating the params.json file.

  -c      --checks        Do checks on balance and existing masternodes
                          offers the possibility to save masternode.conf file.

  -d      --delete        Delete all existing masternodes.
                          must specify correct ticker in params.json

  -r      --create        Create new masternodes with transactions
                          uses transactions from params.json
                          save masternode.conf file automatically at the end.

  -dr     --delcreate     Delete old masternodes and create new ones
                          uses transactions from params.json
                          save masternode.conf file automatically at the end.

  -i      --reindex       Reindex all existing masternodes wallets
                          gives the option to reindex only some of them.
```

# Usage:

```
> python3 masternode_scripts.py [option]
```

only one option at a time is allowed

# Examples:

```
> python3 masternode_scripts.py --checks
```

Will yield the following result:

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

The script comes with an integrated configurator that will help you generate the params.json file.
However the transactions for the creation of new masternodes have to be copied manually from 
your wallet.

An example params.json is provided but not needed. You can delete it and you will be prompted to create
a new one.

The file contains all the parameters needed to use the different functions
* ticker: SAPP, 777, UCR, ODC, etc...
* wallet_data_dir: Path to the data directory of your wallet (directory containing the blockchain and wallet.conf)
* wallet_cli_path: wallet to the `cli` binary
* alias_prefix: prefix for naming the newly created masternodes (default = "MN", so by default the created masternodes 
  will have aliases: MN1, MN2, etc...)
* IHOSTMN-API-KEY: You need to get it from ihostmn so you can connect to your account 
  * visit https://ihostmn.com/settings.php to get your key.
* new_txs: the list of transaction hashes and transaction indexes to create new MNs. 
  You have two options :
  
  1) Simply type in your wallet console `getmasternodeoutputs` and copy/paste the result there
  2) Using the daemon, you can retrieve the transactions using the configurator (see : How to setup the wallet handles)
  
# How to setup the wallet handles:
You should either run the wallet daemon with a -server parameter or add parameters `daemon=1` and `server=1`
to the wallet.conf file of your wallet. This will yield the same result.

Once the wallet.conf edited, simply restart your wallet and wait for it to sync.

The script should now be able to query the wallet. Given that you provided the correct paths in the configuration step.