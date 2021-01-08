from functions.ihostmn import ihostmn
from functions.progress_bar import progress_bar
import time


def delete_all_and_create():

    delete_all_masternodes()

    sleep_time = 30  # in seconds
    print("#### Waiting {}sec before creating new masternodes ...\n".format(sleep_time))
    progress_bar(0, sleep_time)
    for i in range(sleep_time):
        time.sleep(1)
        progress_bar(i + 1, sleep_time)

    create_new_masternodes()


def delete_all_masternodes():
    command = ihostmn()

    #################################
    print("#### Deleting old masternodes ###############################\n")
    #################################

    if command.prompt_confirmation("Are you sure you want to delete all masternodes ? (y/n) : "):
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

    sleep_time = 300  # in seconds
    print("#### Waiting {}sec before retrieving conf file ...".format(sleep_time))
    progress_bar(0, sleep_time)
    for i in range(sleep_time):
        time.sleep(1)
        progress_bar(i + 1, sleep_time)

    # Re-initialization needed to get the new masternodes IDs
    command = ihostmn()

    for mn in command.get_masternodes_list():
        print("Masternode {}-{} : ticker {}\n"
              "  tx id    : {}\n"
              "  tx index : {}\n".format(mn["alias"], mn["id"], mn["ticker"], mn["transaction_id"], mn["tx_index"]))

    command.save_masternode_conf()
