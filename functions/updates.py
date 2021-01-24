from lib.coin_updates import updates


def check_coin_updates(ticker):

    coin_updates = updates(ticker=ticker)

    #################################
    print("#### Checking next coin updates ###################################\n")
    #################################

    coin_updates.start()