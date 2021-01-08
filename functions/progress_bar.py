def progress_bar(iteration, total, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled = int(100 * iteration // total)
    bar = fill * filled + '-' * (100 - filled)
    print(f'\r{bar} | {percent}%', end="\r")
    # Print New Line on Complete
    if iteration == total:
        print("\n")
