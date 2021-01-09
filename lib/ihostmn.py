import sys
import requests
import os
import bcolors
from lib.configurator import configurator


class ihostmn:

    def __init__(self):
        config = configurator()
        self.headers = config.header
        self.ticker = config.ticker
        self.alias_prefix = config.alias_prefix
        self.new_txs = config.new_txs
        self.balance = None
        self.masternodes_list = None
        self.masternodes_conf = None

    def get_balance(self) -> str:
        resp = requests.get("https://ihostmn.com/api/v1/hosting/user/get_balance", headers=self.headers)
        data = resp.json()
        if data["error"] != "":
            print(data["error"])
            sys.exit(1)
        else:
            self.balance = data["result"]["balance"]
            return self.balance

    def get_masternodes_list(self):
        _list = []
        resp = requests.get("https://ihostmn.com/api/v1/hosting/user/list_masternodes", headers=self.headers)
        data = resp.json()
        if data["error"] != "":
            print(data["error"])
            sys.exit(1)
        else:
            for masternode in data["result"]["masternodes"]:
                if self.ticker == masternode["ticker"]:
                    _list.append(masternode)
            self.masternodes_list = _list

    def get_masternodes_conf(self):
        if self.masternodes_list is None:
            self.get_masternodes_list()
        self.masternodes_conf = ""
        for masternode in self.masternodes_list:
            conf = masternode["masternode_conf_text"]
            self.masternodes_conf += conf + "\n"

    def save_masternode_conf(self):
        if self.masternodes_conf is None:
            self.get_masternodes_conf()
        with open('masternode.conf', 'w') as file:
            file.write(self.masternodes_conf)
        print("masternode.conf saved to {}".format(os.getcwd()))

    def delete_masternodes(self):
        if self.masternodes_list is None:
            self.get_masternodes_list()
        for masternode in self.masternodes_list:
            id_ = masternode["id"]
            alias = masternode["alias"]
            resp = requests.post("https://ihostmn.com/api/v1/hosting/user/delete_masternode",
                                 params={"id": id_},
                                 headers=self.headers)
            data = resp.json()
            if data["error"] != "":
                print(data["error"])
                sys.exit(1)
            else:
                if data["result"]["deleted"] == 1:
                    print("Masternode {}-{} deleted\n".format(id_, alias))

    def create_masternodes(self):
        if not self.new_txs:
            print("New transactions for Masternode creation appear to be missing\n"
                  "Please set them manually in params.json then restart\n")
            sys.exit(1)
        else:
            for tx in self.new_txs:
                tx_id = tx["txhash"]
                tx_index = tx["outputidx"]
                alias = self.alias_prefix + str(self.new_txs.index(tx))
                resp = requests.post("https://ihostmn.com/api/v1/hosting/user/create_new_masternode",
                                     params={"cointicker": self.ticker,
                                             "alias": alias,
                                             "txid": tx_id,
                                             "txindex": tx_index,
                                             "dip": 0},
                                     headers=self.headers)
                data = resp.json()
                if data["error"] != "":
                    print(data["error"])
                    sys.exit(1)
                else:
                    new_id = data["result"]["id"]
                    print("Masternode {} with ID {} created\n".format(alias, new_id))

    def reindex_all_masternodes(self):
        if self.masternodes_list is None:
            self.get_masternodes_list()
        for masternode in self.masternodes_list:
            self.reindex_masternode(masternode["id"])

    def reindex_masternode(self, id_):
        resp = requests.post("https://ihostmn.com/api/v1/hosting/user/send_masternode_command",
                             params={"id": id_, "command": "reindex"},
                             headers=self.headers)
        data = resp.json()
        if data["error"] != "":
            print(data["error"])
            sys.exit(1)
        else:
            success = data["result"]["success"]
            if success == 1:
                print("Masternode {} successfully re-indexed\n".format(id_))
            else:
                print("Failed to re-index Masternode {}\n".format(id_))

    def check_block_height(self):
        if self.masternodes_list is None:
            self.get_masternodes_list()
        heights = []
        for mn in self.masternodes_list:
            heights.append(mn["local_blocks"])
            heights.append(mn["remote_blocks"])
        if len(set(heights)) > 1:
            print(f"{bcolors.WARN}Warning: Some block heights are inconsistent, "
                  f"some Masternodes may need reindexing{bcolors.ENDC}\n")

    def print_masternodes(self):
        if self.masternodes_list is None:
            self.get_masternodes_list()
        for mn in self.masternodes_list:
            print("Masternode {}-{} : ticker {}\n"
                  "| tx id        : {}\n"
                  "| tx index     : {}\n"
                  "| block height : {} peers\n"
                  "| | local blocks  - {}\n"
                  "| | remote blocks - {}\n".format(mn["alias"], mn["id"], mn["ticker"],
                                                    mn["transaction_id"],
                                                    mn["tx_index"],
                                                    mn["peers"],
                                                    mn["local_blocks"], mn["remote_blocks"]))

    @staticmethod
    def prompt_confirmation(message) -> bool:
        user_input = ""
        while user_input not in ("y", "n"):
            user_input = input(message).lower()

        return True if user_input == "y" else False
