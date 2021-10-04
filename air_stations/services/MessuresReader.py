

class MessuresReaderInterface():
    def __init__(self, args):
        self.args = list()
        for arg in args:
            self.args.append(arg)
    
    def read_messures(self):
        pass

class MessuresReader1():
    def __init__(self, args):
        super().__init__(args)

    def read_messures(self):
        pass