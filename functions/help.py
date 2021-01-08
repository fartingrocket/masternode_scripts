help_string = "\nmasternode_scripts.py: A script to do all the shitty job when there is a collateral change\n" \
              "                       -> Compatible only with PIVX coins hosted on ihostmn.\n" \
              "                       -> Requires python 3.6 or higher.\n" \
              "                       -> Use at your own risk. No guarantees.\n" \
              "Usage:\n" \
              "\t       python3 masternode_scripts.py [option]\n" \
              "\t       only one option at a time is allowed" \
              "Examples:\n" \
              "\t       python3 masternode_scripts.py --checks\n" \
              "params.json file:\n" \
              "\t       The file contains all the parameters needed to use the different functions\n" \
              "\t       -> ticker: SAPP, 777, UCR, etc...\n" \
              "\t       -> IHOSTMN-API-KEY: You need to get it from ihostmn so you can connect to your account\n" \
              "\t          visit https://ihostmn.com/settings.php to get your key.\n" \
              "\t       -> new_txs: the list of transaction hashes and transaction indexes to create new MNs\n" \
              "\t          simply type in your wallet console 'getmasternodeoutputs' and copy/paste the result\n" \
              "Options:\n" \
              "\t-h\t--help       \tGet this menu.\n" \
              "\t-c\t--checks     \tDo checks on balance and existing masternodes\n" \
              "\t\t\t        and offers the possibility to save masternode.conf file.\n" \
              "\t-d\t--delete     \tDelete all existing masternodes.\n" \
              "\t-r\t--create     \tCreate new masternodes with transactions from params.json\n" \
              "\t\t\t        and save masternode.conf file automatically at the end.\n" \
              "\t-dr\t--delcreate \tDelete old masternodes and create new ones with transactions from params.json\n" \
              "\t\t\t        then save masternode.conf file automatically at the end (combination of -d -r).\n" \
              "\t-i\t--reindex    \tReindex all existing masternodes wallets.\n"
