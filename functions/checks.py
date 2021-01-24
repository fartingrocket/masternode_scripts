from lib.ihostmn import ihostmn
from lib.prompt import prompt_confirmation


def checks(ticker):
    command = ihostmn(ticker=ticker)

    #################################
    print("#### Account Balance ####################################\n")
    #################################

    print("  Current balance = {} EUR\n".format(command.get_balance()))

    #################################
    print("#### List all Masternodes ###############################\n")
    #################################

    mns = command.print_masternodes()

    command.check_block_height()

    #################################
    print("#### Save masternode.conf ##############################\n")
    #################################

    if mns and prompt_confirmation("Do you want to save masternode.conf file ?", default="n"):
        command.save_masternodes_conf()
    elif not mns:
        print("No masternodes configuration to save.\n")
    else:
        print("Save cancelled.\n")
