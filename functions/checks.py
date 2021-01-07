from functions.ihostmn import ihostmn


def checks():
    command = ihostmn()

    #################################
    print("#### Account Balance ####################################\n")
    #################################

    print("  Current balance = {} EUR\n".format(command.get_balance()))

    #################################
    print("#### List all Masternodes ###############################\n")
    #################################

    for mn in command.get_masternodes_list():
        print("Masternode {}-{} : ticker {}\n"
              "  tx id    : {}\n"
              "  tx index : {}\n".format(mn["alias"], mn["id"], mn["ticker"], mn["transaction_id"], mn["tx_index"]))

    #################################
    print("#### Save masternode.conf ##############################\n")
    #################################

    if command.prompt_confirmation("Do you want to save masternode.conf file ? (y/n) : "):
        command.save_masternode_conf()
    else:
        print("Save cancelled.")
