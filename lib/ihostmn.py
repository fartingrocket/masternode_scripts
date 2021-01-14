import sys
import requests
import os
import bcolors
from typing import List

from lib.configurator import configurator
from lib.prompt import prompt_confirmation


class ihostmn:

    def __init__(self):
        self.config = configurator()
        self.config.load()
        self.masternodes_list = None
        self.masternodes_conf = None

    def get_balance(self) -> str:
        resp = requests.get("https://ihostmn.com/api/v1/hosting/user/get_balance", headers=self.config.headers)
        data = resp.json()
        if data["error"] != "":
            print(data["error"])
            sys.exit(1)
        else:
            return data["result"]["balance"]

    @staticmethod
    def get_hosting_price(ticker) -> float:
        resp = requests.get("https://ihostmn.com/api/v1/hosting/public/list_all_coins")
        data = resp.json()
        if data["error"] != "":
            print(data["error"])
            sys.exit(1)
        else:
            for coin in data["result"]["coins"]:
                if coin["ticker"] == ticker:
                    return coin["ticker"]

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

    def save_masternodes_conf(self):
        if self.masternodes_conf is None:
            self.get_masternodes_conf()
        with open('masternode.conf', 'w') as file:
            file.write(self.masternodes_conf)
        print("masternode.conf saved to {}".format(os.getcwd()))

    def delete_all_masternodes(self):
        if self.masternodes_list is None:
            self.get_masternodes_list()
        for masternode in self.masternodes_list:
            self.delete_masternode(alias=masternode["alias"], id_=masternode["id"])

    def delete_masternode(self, alias, id_):
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
        if self.masternodes_list is None:
            self.get_masternodes_list()
        created_new_mn = False
        if self.config.new_txs not in ({}, [], "", None):
            if prompt_confirmation("Transactions found, create Masternodes now ? (y/n) : "):
                mn_counter = 0  # Init value to 0
                for tx in self.config.new_txs:
                    mn_counter += 1
                    alias = self.config.alias_prefix + str(mn_counter)
                    # Check if the transaction is already used in another MN
                    # Useful for the --create option
                    if tx["txhash"] in [mn["transaction_id"] for mn in self.masternodes_list]:
                        print("Transaction : {}\nalready used for another Masternode. Skipping.\n".format(tx["txhash"]))
                    else:
                        # Now we check if the alias is not used for another MN
                        while alias in [mn["alias"] for mn in self.masternodes_list]:
                            mn_counter += 1  # If the alias is there, we increment the counter and create a new alias
                            alias = self.config.alias_prefix + str(mn_counter)
                        self.create_masternode(tx, alias)
                        created_new_mn = True
                if not created_new_mn:
                    print("No new Masternodes were created. Leaving now.\n")
                    sys.exit(0)
            else:
                print("Masternode creation cancelled\n")
                sys.exit(0)
        else:
            # End here if no transactions in params.json
            print("Missing transactions!")
            self.config.set_new_txs()
            self.config.save_params_json()
            self.create_masternodes()

    def create_masternode(self, tx, alias):
        tx_id = tx["txhash"]
        tx_index = tx["outputidx"]
        # Check if sufficient balance before creating masternode
        if float(self.get_balance()) > self.get_hosting_price(self.config.ticker):
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
        else:
            print("Insufficient Balance ! Cannot create Masternode. Leaving.\n")
            sys.exit(0)

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
        heights = list()
        different_chain = False
        need_reindexing = False
        for mn in self.masternodes_list:
            heights.append(mn["local_blocks"])
            heights.append(mn["remote_blocks"])
        # Remove repetitions and sort
        heights = list(set(heights))
        heights.sort()
        # If the wallet handle is set, check wallet block height
        if self.config.wallet_handle and self.config.wallet_handle.check_server():
            wb = self.config.wallet_handle.get_last_block()
            wbh = self.config.wallet_handle.get_block_hash(wb)
            print("Wallet block height : \n"
                  "| block height : {}\n"
                  "| block hash   : {}\n".format(wb, wbh))
            # check if wallet and MNs are on same chain
            h = int(wb) if heights[-1] > int(wb) else heights[-1]
            # We append wallet block height, remove repetitions and sort again
            heights.append(int(wb))
            heights = list(set(heights))
            heights.sort()
            different_chain = (self.get_block_info_by_height(h)["hash"] != wbh)
            if different_chain:
                print(f"{bcolors.WARN}! Wallet and Masternodes appear to be on different chains !{bcolors.ENDC}\n")
            else:
                print(f"{bcolors.BLUE}YAY, Wallet and masternodes on same chain, all good.{bcolors.ENDC}\n")
            need_reindexing = True if (heights[-1] - heights[0] > 5 or different_chain) else False
        else:
            print("Wallet handle not set. Skipping checks on wallet block height."
                  "Use option --configure to setup wallet handle.\n")
            # In case wallet handle is not set, we check block heights on MNs only
            need_reindexing = True if heights[-1] - heights[0] > 5 else False

        if need_reindexing:
            print(f"{bcolors.WARN}! Block heights inconsistent, some Masternodes may need reindexing !{bcolors.ENDC}\n")
            if prompt_confirmation("Reindex now ? ? (y/n) : "):
                self.reindex_all_masternodes()
            else:
                print("Reindex cancelled\n")

    def get_block_info_by_height(self, height):
        resp = requests.get("https://ihostmn.com/api/v1/coinstats/public/getblock",
                            params={"ticker": self.config.ticker, "index": height})
        data = resp.json()
        if data["error"] != "":
            print(data["error"])
            sys.exit(1)
        else:
            return data["result"]["block_info"]

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
