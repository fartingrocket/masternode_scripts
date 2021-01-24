# General description

masternode_scripts is a script to do all the tedious job when there is a collateral change

* Work in progress, please don't mind the bugs (You are welcome to do a Pull Request)
* Compatible only with PIVX based coins (non dip) hosted on ihostmn.
* Requires python 3.6 or higher.
* Use at your own risk. No guarantees.

# Usage

```
> python3 masternode_scripts.py [Argument] [option1] [option2] [option3]
```

see section [Arguments and Options](#arguments-and-options) and [Examples](#examples) for more details.

# Arguments and Options

```

  -h      --help          Get this menu.

  -g      --configure     Starts the configuration manager
                          helps creating the params.json file.

  -k      --checks        Do checks on balance and existing masternodes. Must specify 'ticker' :
                          > python3 masternode_scrypts.py --checks --ticker=SAPP
                          offers the possibility to save masternode.conf file at the end.

  -n      --nextupdate    Calculates when the next update (collateral or reward) will occur.
                          Must specify 'ticker' :
                          > python3 masternode_scrypts.py --nextupdate --ticker=SAPP
                          Requires the API parameters to be set correctly in params.json.

  -d      --delete        Delete one masternode. Must specify 'ticker', 'alias' and 'id' :
                          > python3 masternode_scrypts.py --delete --ticker=SAPP --alias=MN1 --id=12345
                          or
                          > python3 masternode_scrypts.py -d -e SAPP -a MN1 -i 12345
                          Coin must be defined in params.json otherwise you will be prompted to configure it.

  -x      --delete-all    Delete all existing masternodes. Must specify 'ticker' :
                          > python3 masternode_scrypts.py --delete-all --ticker=SAPP
                          Coin must be defined in params.json otherwise you will be prompted to configure it.

  -r      --create        Create new masternodes with transactions. Must specify 'ticker' :
                          > python3 masternode_scrypts.py --create --ticker=SAPP
                          Uses transactions from params.json if defined, otherwise you will be prompted
                          to configure wallet handles
                          Saves masternode.conf file automatically at the end.

  -t      --delcreate     Delete old masternodes and create new ones. Must specify 'ticker' :
                          > python3 masternode_scrypts.py --delcreate --ticker=SAPP
                          Coin must be defined in params.json otherwise you will be prompted to configure it.
                          Saves masternode.conf file automatically at the end.

  -i      --reindex       Reindex all existing masternodes wallets. Must specify 'ticker' :
                          > python3 masternode_scrypts.py --reindex --ticker=SAPP

```

# Examples

```
> python3 masternode_scripts.py --checks --ticker=777
```

Will yield the following result:

```

#### Account Balance ####################################

  Current balance = 15.16 EUR

#### List all Masternodes ###############################

Masternode MN2-XXXXX : ticker 777
| tx id        : o3xs3e02cxxvbp0ujzv5e47nlk0la6ju97dtujvoov20kekmnqh2zvsaimnztcok
| tx index     : 0
| block height : 16 peers
| | local blocks  - 683586
| | remote blocks - 683586

Masternode MN1-XXXXX : ticker 777
| tx id        : sufx1i6rp27neypitm8b2qcykshayxqw1v44vfe5yo1ekx3ciasn7jo0feanjyv3
| tx index     : 0
| block height : 16 peers
| | local blocks  - 683586
| | remote blocks - 683586

Masternode MN3-XXXXX : ticker 777
| tx id        : khro35p0ycdo5m41d29p4cauui2wwqwoa050klhtznmf8o3gcvobw0cr3t0oz1f1
| tx index     : 1
| block height : 16 peers
| | local blocks  - 683586
| | remote blocks - 683586

Wallet block height : 
| block height : 683586
| block hash   : eb8a3a5d6ee062024ba22346d144d3907a131561dae6e9c2859370e4e1f328df

YAY, Wallet and Masternodes on same chain, all good.

#### Save masternode.conf ##############################

Do you want to save masternode.conf file ? (y/n, default=n): y
masternode.conf saved to ~/Documents/masternode_scripts

```

Notice that the block checks will be skipped if the wallet handles are not set.

# params file

The script comes with an integrated configurator that will help you generate the params.json file.

Simply use :

```
> python3 masternode_scripts --configure
```

You will have the choice to either load a previous params.json and complete the missing params, 
or create a new one from scratch (advised), which will overwrite the old one.

An example params.json is provided but not needed. You can delete it and you will be prompted to create
a new one.

The file contains all the parameters needed to use the different functions
* `IHOSTMN-API-KEY`: You need to get it from ihostmn so you can connect to your account
visit https://ihostmn.com/settings.php to get your key.
* `coins`: a dict containing all the coins parameters
name: a free text for the coin name
* `block_average` (optional): URL to retrieve the average block time from the API
* `last_block` (optional): URL to retrieve the last block height from the API
* `max_collateral_at_block`: (optional): block height at which the rewards start decreasing
* `wallet_data_dir`: path to your wallet data dir for this coin
* `wallet_cli_path`: path to your wallet cli (cli name must be included in the path)
* `new_txs`: the list of transaction hashes and transaction indexes to create new MNs. You have two options :
  1) Simply type in your wallet console `getmasternodeoutputs` and copy/paste the result there
  2) Using the daemon, you can retrieve the transactions using the configurator (see : How to setup the wallet handles)
  
# How to setup the wallet handles:

You should either run the wallet daemon with a -server parameter or add parameters `daemon=1` and `server=1`
to the wallet.conf file of your wallet. This will yield the same result.

Once the wallet.conf edited, simply restart your wallet and wait for it to sync.

The script should now be able to query the wallet. Given that you provided the correct paths in the configuration step.
