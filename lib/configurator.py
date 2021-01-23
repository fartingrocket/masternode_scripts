import json
import os
import sys

from lib.prompt import prompt_confirmation
from lib.wallet import wallet


class configurator:
    """
    Allows the load and creation of a params.json file
    """

    def __init__(self):
        self.params_file = os.getcwd() + "/params.json"
        self.ticker = None
        self.wallet_data_dir = ""
        self.wallet_cli_path = ""
        self.wallet_handle = None
        self.headers = None
        self.new_txs = []

    def load(self):

        if os.path.exists(self.params_file) and os.stat(self.params_file).st_size != 0:
            print("\n#### Reading params.json\n")
            with open(self.params_file) as json_file:
                loaded_params = json.load(json_file)
            for param_name, value in loaded_params.items():
                if value not in ({}, [], "", None):
                    if param_name == "headers" and \
                            (value in ({}, [], "", None) or value["IHOSTMN-API-KEY"] in ({}, [], "", None)):
                        print("'{}' value empty in the params.json".format(param_name))
                        self.set_headers()
                    else:
                        setattr(self, param_name, value)
                        print("'{}' found : {}".format(param_name, value))
                # We ignore "wallet_data_dir" and "wallet_cli_path" as these are used for wallet_handle
                # If they are set however, they will be used in chain checks
                elif param_name not in ["wallet_data_dir", "wallet_cli_path"]:
                    print("'{}' value empty in the params.json".format(param_name))
                    call = "set_" + param_name
                    getattr(self, call)()
                else:
                    print("'{}' value empty in the params.json".format(param_name))

            if self.wallet_data_dir and self.wallet_cli_path:
                self.wallet_handle = wallet(data_dir=self.wallet_data_dir, cli_path=self.wallet_cli_path)

            self.save_params_json()
        else:
            print("#### Missing or empty params.json file starting configuration mode\n")
            self.prompt_params_creation()
            self.save_params_json(reload=True)

    def prompt_params_creation(self):

        self.set_ticker()
        self.set_headers()
        if prompt_confirmation("Do you want to use the wallet interface to set transactions ?", default="y"):
            self.set_new_txs()
        else:
            print("\nWallet setup cancelled!\n"
                  "Please enter the transactions manually in params.json before restarting\n")

    def save_params_json(self, reload=False):

        params = {
            "ticker": self.ticker,
            "headers": self.headers,
            "wallet_data_dir": self.wallet_data_dir,
            "wallet_cli_path": self.wallet_cli_path,
            "new_txs": self.new_txs
        }

        with open(self.params_file, 'w') as json_file:
            json.dump(params, json_file, indent=4)

        print("params.json successfully saved\n")

        if reload:
            self.load()

    def set_ticker(self):
        # Ticker
        while not self.ticker:
            self.ticker = input("Input ticker (ex.: SAPP): ").upper()
        return self.ticker

    def set_headers(self):
        # IHOSTMN-API-KEY
        while not self.headers or self.headers["IHOSTMN-API-KEY"] in ({}, [], "", None):
            self.headers = {"IHOSTMN-API-KEY": input("Input your IHOSTMN-API-KEY : ")}

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
                self.save_params_json()
                sys.exit(0)
            else:
                self.set_wallet_handle()
