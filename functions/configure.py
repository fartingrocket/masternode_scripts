from lib.configurator import configurator
from lib.prompt import prompt_confirmation


def configure():

    #################################
    print("#### Starting configuration manager #####################\n")
    #################################
    config = configurator()
    config.read_params_file(prompt_for_creation=False)
    config.prompt_params_creation()
