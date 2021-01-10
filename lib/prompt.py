def prompt_confirmation(message) -> bool:
    user_input = ""
    while user_input not in ("y", "n"):
        user_input = input(message).lower()

    return True if user_input == "y" else False