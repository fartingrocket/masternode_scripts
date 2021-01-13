import getopt
from functions.configure import configure
from functions.checks import checks
from functions.delete_create import *
from functions.reindex import reindex_masternodes
from functions.help import help_string


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hgkdxctra:i:",
                                   ["help", "configure", "checks", "delete", "delete-all", "create", "delcreate",
                                    "reindex", "alias=", "id="])
    except getopt.GetoptError:
        print("Incorrect option(s). use <masternode_scripts.py -h> for help")
        sys.exit(1)
    
    opt = opts[0][0]
    if opt in ("-h", "--help") and len(opts) == 1:
        print(help_string)
    elif opt in ("-g", "--configure") and len(opts) == 1:
        configure()
    elif opt in ("-k", "--checks") and len(opts) == 1:
        checks()
    elif opt in ("-d", "--delete") and len(opts) == 3:
        if opts[1][0] in ("-a", "--alias") and opts[2][0] in ("-i", "--id"):
            delete_one_masternode(opts[1][1], opts[2][1])
        else:
            print("Missing or incorrect argument(s). use <masternode_scripts.py -h> for help")
            sys.exit(2)
    elif opt in ("-x", "--delete-all") and len(opts) == 1:
        delete_all_masternodes()
    elif opt in ("-c", "--create") and len(opts) == 1:
        create_new_masternodes()
    elif opt in ("-t", "--delcreate") and len(opts) == 1:
        delete_all_and_create()
    elif opt in ("-r", "--reindex") and len(opts) == 1:
        reindex_masternodes()
    else:
        print("Too many arguments. use <masternode_scripts.py -h> for help")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
