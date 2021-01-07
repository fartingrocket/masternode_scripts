from functions.ihostmn import ihostmn
import time


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

    print("Waiting 30 sec before creating new masternodes ...\n")
    time.sleep(30)

    command.create_masternodes()

    #################################
    print("#### Getting Masternode.conf ###############################\n")
    #################################

    print("#### Waiting 5 minutes before getting the Masternode.conf ...")
    time.sleep(300)

    # Re-initialization needed to get the new masternodes IDs
    print("#### Re-initializing ...\n")
    command = ihostmn()

    for mn in command.get_masternodes_list():
        print("Masternode {}-{} : ticker {}\n"
              "  tx id    : {}\n"
              "  tx index : {}\n".format(mn["alias"], mn["id"], mn["ticker"], mn["transaction_id"], mn["tx_index"]))

    command.save_masternode_conf()
