import getopt

from functions.checks import checks
from functions.configure import configure
from functions.delete_create import *
from functions.help import help_string
from functions.reindex import reindex_masternodes
from functions.updates import check_coin_updates


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hgkdxctrna:i:e:",
                                   ["help", "configure", "checks", "delete", "delete-all", "create", "delcreate",
                                    "reindex", "nextupdate", "ticker=", "alias=", "id="])
    except getopt.GetoptError:
        print("Incorrect option(s). use <masternode_scripts.py -h> for help")
        sys.exit(1)

    try:
        if opts[0][0] in ("-h", "--help") and len(opts) == 1:
            print(help_string)
        elif opts[0][0] in ("-g", "--configure") and len(opts) == 1:
            configure()
        elif opts[0][0] in ("-k", "--checks") and opts[1][0] in ("-e", "--ticker") and len(opts) == 2:
            checks(ticker=opts[1][1])
        elif opts[0][0] in ("-n", "--nextupdate") and opts[1][0] in ("-e", "--ticker") and len(opts) == 2:
            check_coin_updates(ticker=opts[1][1])
        elif opts[0][0] in ("-d", "--delete") and opts[1][0] in ("-e", "--ticker") and len(opts) == 3:
            if opts[2][0] in ("-a", "--alias") and opts[3][0] in ("-i", "--id"):
                delete_one_masternode(ticker=opts[1][1], alias=opts[2][1], id_=opts[3][1])
            elif opts[2][0] in ("-i", "--id") and opts[3][0] in ("-a", "--alias"):
                delete_one_masternode(ticker=opts[1][1], alias=opts[3][1], id_=opts[2][1])
        elif opts[0][0] in ("-x", "--delete-all") and opts[1][0] in ("-e", "--ticker") and len(opts) == 2:
            delete_all_masternodes(ticker=opts[1][1])
        elif opts[0][0] in ("-c", "--create") and opts[1][0] in ("-e", "--ticker") and len(opts) == 2:
            create_new_masternodes(ticker=opts[1][1])
        elif opts[0][0] in ("-t", "--delcreate") and opts[1][0] in ("-e", "--ticker") and len(opts) == 2:
            delete_all_and_create(ticker=opts[1][1])
        elif opts[0][0] in ("-r", "--reindex") and opts[1][0] in ("-e", "--ticker") and len(opts) == 2:
            reindex_masternodes(ticker=opts[1][1])
    except IndexError:
        print("Incorrect option(s). use <masternode_scripts.py -h> for help")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
