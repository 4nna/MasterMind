

class SimpleAI():

    def __init__(self, mind):
        self.mind = mind

    def guess(self):
        return [int(c) for c in self.mind.get_guess(smart=True)]

