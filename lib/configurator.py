import json
import os
import sys

import bcolors

from lib.prompt import prompt_confirmation
from lib.wallet import wallet


class configurator:
    """
    Allows the load and creation of a params.json file
    """

    def __init__(self):
        self.params_path = os.getcwd() + "/params.json"
        self.params_file = None
        self.loaded_coin_params = None
        # REST params
        self.headers = None
        # coin params
        self.ticker = None
        self.name = None
        self.block_average = None
        self.last_block = None
        self.update_interval = None
        self.max_collateral_at_block = None
        self.wallet_data_dir = None
        self.wallet_cli_path = None
        self.wallet_handle = None
        self.new_txs = []

    def read_params(self):
        if os.path.exists(self.params_path) and os.stat(self.params_path).st_size != 0:
            print("#### Reading params.json\n")
            with open(self.params_path) as json_file:
                self.params_file = json.load(json_file)
            for param, values in self.params_file.items():
                if param == "coins":
                    for coin, coin_param in values.items():
                        if coin == self.ticker:
                            self.loaded_coin_params = coin_param
                elif param == "headers":
                    if values in ({}, [], "", None) or values["IHOSTMN-API-KEY"] in ({}, [], "", None):
                        print("'{}'".format(param) + f" value {bcolors.FAIL}missing{bcolors.END}")
                        self.set_headers()
                    else:
                        self.headers = values
                        print("param 'headers'" + f" {bcolors.PASS} found {bcolors.END}")
        else:
            print("#### Missing or empty params.json file starting configuration mode\n")
            self.prompt_params_creation()

    def load(self, ticker):
        self.ticker = ticker
        self.read_params()
        need_save = False
        for param_name, value in self.loaded_coin_params.items():
            if value not in ({}, [], "", None, 0):
                setattr(self, param_name, value)
                print("param '{}'".format(param_name)+f" {bcolors.PASS} found {bcolors.END}")
            # We ignore "wallet_data_dir" and "wallet_cli_path" as these are used for wallet_handle
            # They will be set when user prompted to set wallet_handle
            # If they are set however, they will be used in chain checks
            elif param_name not in ["wallet_data_dir", "wallet_cli_path"]:
                print("param '{}'".format(param_name) + f" value {bcolors.FAIL}missing{bcolors.END}")
                call = "set_" + param_name
                getattr(self, call)()
                need_save = True
            else:
                print("'{}' value empty in the params.json".format(param_name))

        if self.wallet_data_dir and self.wallet_cli_path:
            self.wallet_handle = wallet(data_dir=self.wallet_data_dir, cli_path=self.wallet_cli_path)

        if need_save:
            self.save_params_json()
        else:
            print()

    def prompt_params_creation(self):

        self.set_headers()
        self.set_ticker()
        self.set_name()
        self.set_block_average()
        self.set_last_block()
        self.set_update_interval()
        self.set_max_collateral_at_block()

        if prompt_confirmation("Do you want to use the wallet interface to set transactions ?", default="y"):
            self.set_new_txs()
        else:
            print("\nWallet setup cancelled!\n"
                  "Please enter the transactions manually in params.json before restarting\n")

        self.save_params_json(reload=True)

    def save_params_json(self, reload=False):

        coin = {
                self.ticker: {
                    "name": self.name,
                    "block_average": self.block_average,
                    "last_block": self.last_block,
                    "update_interval": self.update_interval,
                    "max_collateral_at_block": self.max_collateral_at_block,
                    "wallet_data_dir": self.wallet_data_dir,
                    "wallet_cli_path": self.wallet_cli_path,
                    "new_txs": self.new_txs
                }
        }

        headers = {
            "headers": self.headers,
        }

        if not self.params_file:
            self.params_file = {"headers": None, "coins": {}}
        self.params_file.update(headers)
        self.params_file["coins"].update(coin)

        with open(self.params_path, 'w') as json_file:
            json.dump(self.params_file, json_file, indent=4)

        print("\nparams.json successfully saved\n")

        if reload:
            self.load(self.ticker)

    def set_ticker(self):
        # Ticker
        while not self.ticker:
            self.ticker = input("Input ticker (ex.: SAPP): ").upper()

    def set_headers(self):
        # IHOSTMN-API-KEY
        while not self.headers or self.headers["IHOSTMN-API-KEY"] in ({}, [], "", None):
            self.headers = {"IHOSTMN-API-KEY": input("Input your IHOSTMN-API-KEY : ")}

    def set_name(self):
        while not self.name:
            self.name = input("Input coin name (ex.: SAPPHIRE) (free text) : ").upper()

    def set_block_average(self):
        resp = input("Input URL to coin API to retrieve block avg time (optional) : ")
        self.block_average = "" if resp in ({}, [], "", None) else resp

    def set_last_block(self):
        resp = input("Input URL to coin API to retrieve last block count (optional) : ")
        self.last_block = "" if resp in ({}, [], "", None) else resp

    def set_update_interval(self):
        resp = input("Input interval block number between updates (ex. for SAPP: 50000) (optional) : ")
        self.update_interval = 0 if resp in ({}, [], "", None, 0) else int(resp)

    def set_max_collateral_at_block(self):
        resp = input("Input block height at which rewards start decreasing (ex. for SAPP: 700000) (optional) : ")
        self.max_collateral_at_block = 0 if resp in ({}, [], "", None, 0) else int(resp)

    def set_new_txs(self):
        # Transactions list for MN creation
        # These 'If' conditions need to be nested.
        # We first check for handle then we check connection with wallet
        if self.wallet_handle:
            if self.wallet_handle.check_server():
                self.new_txs = json.loads(self.wallet_handle.get_masternode_outputs())
                print("Transactions retrieved from wallet:\n"
                      "{}".format(self.new_txs))
            else:
                print("Cannot connect to wallet.\n"
                      "Please check your wallet configuration or enter the transactions manually in params.json\n")
                self.new_txs = []
                self.save_params_json()
                sys.exit(0)
        else:
            print("Wallet handle missing.")
            self.set_wallet_handle()
            self.set_new_txs()

    def set_wallet_handle(self):
        # Setup the wallet handle to get transaction from the wallet
        if not self.wallet_data_dir:
            self.wallet_data_dir = input("Input the path to {} data directory : ".format(self.ticker))
        if not self.wallet_cli_path:
            self.wallet_cli_path = input("Input the path to the {} cli binary : ".format(self.ticker))

        # Initiate the wallet handle if the paths are not empty
        if self.wallet_data_dir not in ({}, [], "", None) and self.wallet_cli_path not in ({}, [], "", None):
            self.wallet_handle = wallet(data_dir=self.wallet_data_dir, cli_path=self.wallet_cli_path)
        else:
            if prompt_confirmation("Entered paths to the data directory and/or cli binary are empty !\n"
                                   "Do you wish to Cancel wallet setup ?", default="y"):
                print("\nWallet setup cancelled!\n"
                      "Please enter the transactions manually in params.json before restarting\n")
                # Save before exit to keep data that was added during config
                self.wallet_data_dir = ""
                self.wallet_cli_path = ""
                self.save_params_json()
                sys.exit(0)
            else:
                self.set_wallet_handle()
