from lib.ihostmn import ihostmn


def checks():
    command = ihostmn()

    #################################
    print("#### Account Balance ####################################\n")
    #################################

    print("  Current balance = {} EUR\n".format(command.get_balance()))

    #################################
    print("#### List all Masternodes ###############################\n")
    #################################

    command.print_masternodes()

    #################################
    print("#### Save masternode.conf ##############################\n")
    #################################

    if command.prompt_confirmation("Do you want to save masternode.conf file ? (y/n) : "):
        command.save_masternode_conf()
    else:
        print("Save cancelled.")
