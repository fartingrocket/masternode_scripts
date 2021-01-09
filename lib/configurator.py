import json
import os


class configurator:
    """
    Allows the load and creation of a params.json file
    """

    def __init__(self):
        self.ticker = None
        self.alias_prefix = None
        self.header = None
        self.new_txs = None
        self.load()

    def load(self):
        params_file = os.getcwd() + "/params.json"
        if os.path.exists(params_file):
            with open(params_file) as json_file:
                params = json.load(json_file)
            self.ticker = params["ticker"]
            self.alias_prefix = params["alias_prefix"]
            self.header = params["header"]
            self.new_txs = params["new_txs"]
        else:
            print("#### Missing params.json file entering configuration mode\n")
            self.prompt_params_creation()

    def prompt_params_creation(self):

        # Ticker
        _ticker = None
        while not _ticker:
            _ticker = input("Input ticker (ex.: SAPP): ").upper()

        # Alias prefix
        inp_alias = input("Input alias prefix for masternodes (Press enter for default = 'MN') : ").upper()
        _alias_prefix = "MN" if not inp_alias else inp_alias

        # IHOSTMN-API-KEY
        _api_key = None
        while not _api_key:
            _api_key = input("Input your IHOSTMN-API-KEY : ")

        # Init new_txs list to empty
        _new_txs = []

        params = {
            "ticker": _ticker,
            "alias_prefix": _alias_prefix,
            "header": {"IHOSTMN-API-KEY": _api_key},
            "new_txs": []
        }

        with open(os.getcwd() + "/params.json", 'w') as json_file:
            json.dump(params, json_file, indent=4)

        input("\nparams.json successfully created\n"
              "New transactions for Masternode creation have to be set manually\n"
              "Please copy the result of 'getmasternodeoutputs' from your wallet console in params.json\n"
              "You can do it now or you can Press 'Enter' to continue anyway.\n")

        self.load()
