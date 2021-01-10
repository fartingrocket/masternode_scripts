import subprocess
import sys


class wallet:

    def __init__(self, data_dir=None, cli_path=None):
        self.cli_path = cli_path
        self.data_dir = data_dir

    def check_server(self) -> bool:
        check = subprocess.run([self.cli_path,
                                "-datadir=" + self.data_dir,
                                "getinfo"],
                               stdout=subprocess.DEVNULL)

        return True if check.returncode == 0 else False

    def get_masternode_outputs(self):

        masternodeoutputs = subprocess.run([self.cli_path,
                                            "-datadir=" + self.data_dir,
                                            "getmasternodeoutputs"],
                                           stdout=subprocess.PIPE)

        if masternodeoutputs.returncode == 0:
            return masternodeoutputs.stdout.decode().rstrip()
        else:
            return []
