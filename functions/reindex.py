from lib.ihostmn import ihostmn


def reindex_masternodes():
    command = ihostmn()

    #################################
    print("#### Reindexing Masternodes wallets ###############################\n")
    #################################

    command.print_masternodes()

    if command.prompt_confirmation("Do you want to reindex all or individually ? 'y' for all (y/n) : "):
        command.reindex_all_masternodes()
    else:
        id_ = input("Please input the index (Leave empty and press 'Enter' to quit): ")
        while id_:
            command.reindex_masternode(id_)
            id_ = input("Please input the index (Leave empty and press 'Enter' to quit): ")
