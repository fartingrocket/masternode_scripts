import bcolors

help_string = f"\n{bcolors.BOLD}masternode_scripts.py:{bcolors.END}\n" \
              "\t       A script to do all the tedious job when there is a collateral change\n" \
              "\t         -> Compatible only with PIVX based coins (non dip) hosted on ihostmn.\n" \
              "\t         -> Requires python 3.6 or higher.\n" \
              "\t         -> Use at your own risk. No guarantees.\n\n" \
              f"{bcolors.BOLD}Usage:{bcolors.END}\n" \
              "\t       > python3 masternode_scripts.py [Argument] [option1] [option2] [option3]\n" \
              f"\t       See {bcolors.BOLD}'Arguments and Options'{bcolors.END} section for details and examples.\n\n" \
              f"{bcolors.BOLD}Examples:{bcolors.END}\n" \
              "\t       > python3 masternode_scripts.py --checks\n\n" \
              f"{bcolors.BOLD}params.json file:{bcolors.END}\n" \
              "\t       The file contains all the parameters needed to use the different functions\n" \
              "\t       -> IHOSTMN-API-KEY: You need to get it from ihostmn so you can connect to your account\n" \
              "\t          visit https://ihostmn.com/settings.php to get your key.\n" \
              "\t       -> coins: a dict containing all the coins parameters\n" \
              "\t       |--> name: a free text for the coin name\n" \
              "\t       |--> block_average (optional): URL to retrieve the average block time from the API\n" \
              "\t       |--> last_block (optional): URL to retrieve the last block height from the API\n" \
              "\t       |--> max_collateral_at_block (optional): block height at which the rewards start decreasing\n" \
              "\t       |--> wallet_data_dir : path to your wallet data dir for this coin\n" \
              "\t       |--> wallet_cli_path : path to your wallet cli (cli name must be included in the path)\n" \
              "\t       |--> new_txs: the list of transaction hashes and transaction indexes to create new MNs\n" \
              "\t            simply type in your wallet console 'getmasternodeoutputs' and copy/paste the result\n\n" \
              "\t       A sample file is provided.\n" \
              "\t       Use `--configure` option to help you create the params.json file.\n\n" \
              f"{bcolors.BOLD}Arguments and Options:{bcolors.END}\n" \
              "\t-h \t--help       \tGet this menu.\n\n" \
              "\t-g \t--configure  \tStarts the configuration manager\n" \
              "\t\t\t        helps creating the params.json file.\n\n" \
              "\t-k \t--checks     \tDo checks on balance and existing masternodes. Must specify `ticker` :\n" \
              "\t\t\t        > python3 masternode_scrypts.py --checks --ticker=SAPP\n" \
              "\t\t\t        offers the possibility to save masternode.conf file at the end.\n\n" \
              "\t-n \t--nextupdate \tCalculates when the next update (collateral or reward) will occur.\n" \
              "\t\t\t        Must specify `ticker` :\n" \
              "\t\t\t        > python3 masternode_scrypts.py --nextupdate --ticker=SAPP\n" \
              "\t\t\t        Requires the API parameters to be set correctly in params.json.\n\n" \
              "\t-d \t--delete     \tDelete one masternode. Must specify `ticker`, `alias` and `id` :\n" \
              "\t\t\t        > python3 masternode_scrypts.py --delete --ticker=SAPP --alias=MN1 --id=12345\n" \
              "\t\t\t        or\n" \
              "\t\t\t        > python3 masternode_scrypts.py -d -e SAPP -a MN1 -i 12345\n" \
              "\t\t\t        Coin must be defined in params.json otherwise you will be prompted to configure it.\n\n" \
              "\t-x \t--delete-all \tDelete all existing masternodes. Must specify `ticker` :\n" \
              "\t\t\t        > python3 masternode_scrypts.py --delete-all --ticker=SAPP\n" \
              "\t\t\t        Coin must be defined in params.json otherwise you will be prompted to configure it.\n\n" \
              "\t-r \t--create     \tCreate new masternodes with transactions. Must specify `ticker` :\n" \
              "\t\t\t        > python3 masternode_scrypts.py --create --ticker=SAPP\n" \
              "\t\t\t        Uses transactions from params.json if defined, otherwise you will be prompted\n" \
              "\t\t\t        to configure wallet handles\n" \
              "\t\t\t        Saves masternode.conf file automatically at the end.\n\n" \
              "\t-t\t--delcreate   \tDelete old masternodes and create new ones. Must specify `ticker` :\n" \
              "\t\t\t        > python3 masternode_scrypts.py --delcreate --ticker=SAPP\n" \
              "\t\t\t        Coin must be defined in params.json otherwise you will be prompted to configure it.\n" \
              "\t\t\t        Saves masternode.conf file automatically at the end.\n\n" \
              "\t-i \t--reindex    \tReindex all existing masternodes wallets. Must specify `ticker` :\n" \
              "\t\t\t        > python3 masternode_scrypts.py --reindex --ticker=SAPP\n" \
