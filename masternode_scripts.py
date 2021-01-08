from functions.checks import checks
from functions.delete_create import delete_all_and_create, delete_all_masternodes, create_new_masternodes
from functions.reindex_all import reindex_all_masternodes
from functions.help import help_string
import sys


def main(argv):
    if not argv:
        print("Missing argument. use <masternode_scripts.py -h> for help")
        sys.exit(1)
    for arg in argv:
        if arg in ("-h", "--help"):
            print(help_string)
            sys.exit()
        elif arg in ("-c", "--checks"):
            checks()
        elif arg in ("-d", "--delete"):
            delete_all_masternodes()
        elif arg in ("-r", "--create"):
            create_new_masternodes()
        elif arg in ("-dr", "--delcreate"):
            delete_all_and_create()
        elif arg in ("-i", "--reindex"):
            reindex_all_masternodes()
        else:
            print("Incorrect argument. use <masternode_scripts.py -h> for help")
            sys.exit(2)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Too many arguments. use <masternode_scripts.py -h> for help")
        sys.exit(2)
    main(sys.argv[1:2])
