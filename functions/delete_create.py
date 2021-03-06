import sys

from lib.ihostmn import ihostmn
from lib.prompt import prompt_confirmation
from .progress_bar import print_progress


def delete_all_and_create(ticker):

    if delete_all_masternodes(ticker=ticker):
        # After deleting all, waiting 30sec before creating new masternodes
        print_progress(30)
    else:
        # End here if deletion cancelled
        if not prompt_confirmation("Do you still wish to proceed and create new Masternodes ?", default="n"):
            print("Masternode creation cancelled. Aborting.\n")
            sys.exit(0)

    create_new_masternodes(ticker=ticker)


def delete_all_masternodes(ticker) -> bool:
    command = ihostmn(ticker=ticker)

    #################################
    print("#### Deleting old masternodes ###############################\n")
    #################################

    if prompt_confirmation("Are you sure you want to delete all masternodes ?", default="n"):
        command.delete_all_masternodes()
        return True
    else:
        print("Deletion cancelled.\n")
        return False


def delete_one_masternode(ticker, alias, id_) -> bool:
    command = ihostmn(ticker=ticker)

    #################################
    print("#### Deleting masternode ####################################\n")
    #################################

    if prompt_confirmation("Are you sure you want to delete masternode {} : {} ?".format(alias, id_), default="n"):
        command.delete_masternode(alias=alias, id_=id_)
        return True
    else:
        print("Deletion cancelled.\n")
        return False


def create_new_masternodes(ticker):
    command = ihostmn(ticker=ticker)

    #################################
    print("#### Creating new masternodes ###############################\n")
    #################################

    command.create_masternodes()

    #################################
    print("#### Getting Masternode.conf ###############################\n")
    #################################

    # Waiting 180sec before retrieving conf file
    print_progress(180)

    # Get the new masternodes IDs
    command.get_masternodes_list()

    command.print_masternodes()

    command.save_masternodes_conf()
