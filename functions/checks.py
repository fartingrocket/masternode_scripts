from lib.ihostmn import ihostmn
from lib.prompt import prompt_confirmation


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

    command.check_block_height()

    #################################
    print("#### Save masternode.conf ##############################\n")
    #################################

    if prompt_confirmation("Do you want to save masternode.conf file ?", default="n"):
        command.save_masternodes_conf()
    else:
        print("Save cancelled.")
