from functions.ihostmn import ihostmn


def reindex_all_masternodes():
    command = ihostmn()

    #################################
    print("#### Reindexing all Masternodes wallets ###############################\n")
    #################################

    command.reindex_masternodes()
