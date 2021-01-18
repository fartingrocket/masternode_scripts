def prompt_confirmation(message, true_value="y", false_value="n", default="n") -> bool:
    user_input = None
    while user_input not in (true_value, false_value, default):
        user_input = input(message+" ({}/{}, default={}): ".format(true_value, false_value, default)).lower()
        if not user_input:
            user_input = default

    return True if user_input == true_value else False
