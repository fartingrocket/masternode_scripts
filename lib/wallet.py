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

    def get_last_block(self):

        get_block_count = subprocess.run([self.cli_path, "-datadir=" + self.data_dir, "getblockcount"],
                                         stdout=subprocess.PIPE)

        if get_block_count.returncode == 0:
            return get_block_count.stdout.decode().rstrip()
        else:
            return None

    def get_block_hash(self, block=None):
        last_block = block if block is not None else self.get_last_block
        get_block_hash = subprocess.run(
            [self.cli_path, "-datadir=" + self.data_dir, "getblockhash", last_block],
            stdout=subprocess.PIPE)

        if get_block_hash.returncode == 0:
            return get_block_hash.stdout.decode().rstrip()
        else:
            return None
