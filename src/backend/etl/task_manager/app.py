from manager import Manager

# parse command line arguments
# if cli flag then run cli
def main():
    # main2 script
    manager = Manager()
    manager.run()

    # if flag render cli
    app = App(manager)
    # app fetchtes all data from manager
    app.render()
    # on new job
        # pause schedule
        # add job to ledger
        # reload ledger
        # re run scheduler based on new ledger
        # update schedule
        # resume schedule
            # add tasks to queue


class App:
    def __init__(self, manager: Manager)):
        self.manager = manager

    def render(self):
        ...
