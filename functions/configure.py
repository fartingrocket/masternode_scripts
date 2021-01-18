from lib.configurator import configurator
from lib.prompt import prompt_confirmation


def configure():

    #################################
    print("#### Starting configuration manager #####################\n")
    #################################
    config = configurator()
    if prompt_confirmation("Do you want to load an existing params.json to complete missing params ?", default="y"):
        config.load()
        if config.new_txs in ({}, [], "", None):
            print("Missing transactions!")
            config.set_new_txs()
            config.save_params_json()
    else:
        config.prompt_params_creation()
        config.save_params_json()


