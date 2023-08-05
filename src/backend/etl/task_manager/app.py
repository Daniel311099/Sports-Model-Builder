from manager import Manager

# parse command line arguments
# if cli flag then run cli
def main():
    manager = Manager()
    # main2 script
    job = input('Enter job: ')
    # on new job
        # pause schedule
        # add job to ledger
        # reload ledger
        # re run scheduler based on new ledger
        # update schedule
        # resume schedule
            # add tasks to queue