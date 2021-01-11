import sys
import requests
import os
import bcolors
from lib.configurator import configurator
from lib.prompt import prompt_confirmation


class ihostmn:

    def __init__(self):
        self.config = configurator()
        self.config.load()
        self.balance = None
        self.masternodes_list = None
        self.masternodes_conf = None

    def get_balance(self) -> str:
        resp = requests.get("https://ihostmn.com/api/v1/hosting/user/get_balance", headers=self.config.headers)
        data = resp.json()
        if data["error"] != "":
            print(data["error"])
            sys.exit(1)
        else:
            self.balance = data["result"]["balance"]
            return self.balance

    def get_masternodes_list(self):
        _list = []
        resp = requests.get("https://ihostmn.com/api/v1/hosting/user/list_masternodes", headers=self.config.headers)
        data = resp.json()
        if data["error"] != "":
            print(data["error"])
            sys.exit(1)
        else:
            for masternode in data["result"]["masternodes"]:
                if self.config.ticker == masternode["ticker"]:
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
                                 headers=self.config.headers)
            data = resp.json()
            if data["error"] != "":
                print(data["error"])
                sys.exit(1)
            else:
                if data["result"]["deleted"] == 1:
                    print("Masternode {}-{} deleted\n".format(id_, alias))

    def create_masternodes(self):
        if self.config.new_txs and self.config.new_txs not in ({}, [], "", None):
            if prompt_confirmation("Transactions found, create Masternodes now ? (y/n) : "):
                for tx in self.config.new_txs:
                    self.create_masternode(tx)
            else:
                print("Masternode creation cancelled\n")
                sys.exit(0)
        else:
            # End here if no transactions in params.json and user cancels wallet interface
            if prompt_confirmation("Missing transactions\nDo you want to use the wallet interface ? (y/n) : "):
                self.config.set_new_txs()
            else:
                print("\nWallet setup cancelled!\n"
                      "Please enter the transactions manually in params.json before restarting\n")
                sys.exit(1)

    def create_masternode(self, tx):
        tx_id = tx["txhash"]
        tx_index = tx["outputidx"]
        alias = self.config.alias_prefix + str(self.config.new_txs.index(tx))
        resp = requests.post("https://ihostmn.com/api/v1/hosting/user/create_new_masternode",
                             params={"cointicker": self.config.ticker,
                                     "alias": alias,
                                     "txid": tx_id,
                                     "txindex": tx_index,
                                     "dip": 0},
                             headers=self.config.headers)
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
        # print a new line when all done
        print()

    def reindex_masternode(self, id_):
        resp = requests.post("https://ihostmn.com/api/v1/hosting/user/send_masternode_command",
                             params={"id": id_, "command": "reindex"},
                             headers=self.config.headers)
        data = resp.json()
        if data["error"] != "":
            print(data["error"])
            sys.exit(1)
        else:
            success = data["result"]["success"]
            if success == 1:
                print("Masternode {} successfully re-indexed".format(id_))
            else:
                print("Failed to re-index Masternode {}".format(id_))

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
            if prompt_confirmation("Reindex now ? ? (y/n) : "):
                self.reindex_all_masternodes()
            else:
                print("Reindex cancelled\n")

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
