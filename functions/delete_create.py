import sys
from lib.ihostmn import ihostmn
from functions.progress_bar import print_progress
from lib.prompt import prompt_confirmation


def delete_all_and_create():

    if delete_all_masternodes():
        # After deleting all, waiting 30sec before creating new masternodes
        print_progress(30)
    else:
        # End here if deletion cancelled
        if not prompt_confirmation("Do you still wish to proceed to create new Masternodes ? (y/n) : "):
            print("Masternode creation cancelled. Aborting.\n")
            sys.exit(0)

    create_new_masternodes()


def delete_all_masternodes() -> bool:
    command = ihostmn()

    #################################
    print("#### Deleting old masternodes ###############################\n")
    #################################

    if prompt_confirmation("Are you sure you want to delete all masternodes ? (y/n) : "):
        command.delete_masternodes()
        return True
    else:
        print("Deletion cancelled.\n")
        return False


def create_new_masternodes():
    command = ihostmn()

    #################################
    print("#### Creating new masternodes ###############################\n")
    #################################

    command.create_masternodes()

    #################################
    print("#### Getting Masternode.conf ###############################\n")
    #################################

    # Waiting 120sec before retrieving conf file
    print_progress(120)

    # Get the new masternodes IDs
    command.get_masternodes_list()

    command.print_masternodes()

    command.save_masternode_conf()
