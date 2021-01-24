from lib.ihostmn import ihostmn
from lib.prompt import prompt_confirmation


def reindex_masternodes(ticker):
    command = ihostmn(ticker=ticker)

    #################################
    print("#### Reindexing Masternodes wallets ###############################\n")
    #################################

    command.print_masternodes()

    if prompt_confirmation("Do you want to reindex all or individually ? 'a' for all",
                           true_value="a", false_value="i", default="i"):
        command.reindex_all_masternodes()
    else:
        id_ = input("Please input the index (Leave empty and press 'Enter' to quit): ")
        while id_:
            command.reindex_masternode(id_)
            id_ = input("Please input the index (Leave empty and press 'Enter' to quit): ")
