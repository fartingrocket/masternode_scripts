import requests
import json
import os


class ihostmn:

    def __init__(self):
        with open(os.getcwd()+"/params.json") as json_file:
            global_params = json.load(json_file)
        self.headers = global_params["header"]
        self.ticker = global_params["ticker"]
        self.alias_prefix = global_params["alias_prefix"]
        self.new_txs = global_params["new_txs"]
        self.balance = None
        self.masternodes_list = None
        self.masternodes_conf = None

    def get_balance(self):
        resp = requests.get("https://ihostmn.com/api/v1/hosting/user/get_balance", headers=self.headers)
        data = resp.json()
        self.balance = data["result"]["balance"]
        return self.balance

    def get_masternodes_list(self):
        _list = []
        resp = requests.get("https://ihostmn.com/api/v1/hosting/user/list_masternodes", headers=self.headers)
        data = resp.json()
        for masternode in data["result"]["masternodes"]:
            if self.ticker == masternode["ticker"]:
                _list.append(masternode)
        self.masternodes_list = _list
        return self.masternodes_list

    def get_masternodes_conf(self):
        if self.masternodes_list is None:
            self.get_masternodes_list()
        self.masternodes_conf = ""
        for masternode in self.masternodes_list:
            conf = masternode["masternode_conf_text"]
            self.masternodes_conf += conf + "\n"
        return self.masternodes_conf

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
            if data["result"]["deleted"] == 1:
                print("Masternode {}-{} deleted\n".format(id_, alias))

    def create_masternodes(self):
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
            new_id = data["result"]["id"]
            print("Masternode {} with ID {} created\n".format(alias, new_id))

    def reindex_masternodes(self):
        if self.masternodes_list is None:
            self.get_masternodes_list()
        for masternode in self.masternodes_list:
            id_ = masternode["id"]
            alias = masternode["alias"]
            resp = requests.post("https://ihostmn.com/api/v1/hosting/user/send_masternode_command",
                                 params={"id": id_, "command": "reindex"},
                                 headers=self.headers)
            data = resp.json()
            success = data["result"]["success"]
            if success == 1:
                print("Masternode {}-{} successfully re-indexed\n".format(alias, id_))
            else:
                print("Failed to re-index Masternode {}-{}\n".format(alias, id_))

    def print_masternodes(self):
        if self.masternodes_list is None:
            self.get_masternodes_list()
        for mn in self.masternodes_list():
            print("Masternode {}-{} : ticker {}\n"
                  "  tx id    : {}\n"
                  "  tx index : {}\n".format(mn["alias"], mn["id"], mn["ticker"], mn["transaction_id"], mn["tx_index"]))

    @staticmethod
    def prompt_confirmation(message):
        user_input = ""
        while user_input not in ("y", "n"):
            user_input = input(message).lower()

        return True if user_input == "y" else False
