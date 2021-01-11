from lib.ihostmn import ihostmn
from functions.progress_bar import print_progress
from lib.prompt import prompt_confirmation


def delete_all_and_create():

    delete_all_masternodes()

    # Waiting 30sec before creating new masternodes
    print_progress(30)

    create_new_masternodes()


def delete_all_masternodes():
    command = ihostmn()

    #################################
    print("#### Deleting old masternodes ###############################\n")
    #################################

    if prompt_confirmation("Are you sure you want to delete all masternodes ? (y/n) : "):
        command.delete_masternodes()
    else:
        print("Deletion cancelled.")


def create_new_masternodes():
    command = ihostmn()

    #################################
    print("#### Creating new masternodes ###############################\n")
    #################################

    command.create_masternodes()

    #################################
    print("#### Getting Masternode.conf ###############################\n")
    #################################

    # Waiting 300sec before retrieving conf file
    print_progress(300)

    # Get the new masternodes IDs
    command.get_masternodes_list()

    command.print_masternodes()

    command.save_masternode_conf()
