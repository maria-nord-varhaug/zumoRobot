from bbcon import Bbcon

#tar imot motorforespørsler fra behaviour, og bestemmer hvilke som skal bli utført :)

class Arbitrator():

    def __init__(self, bbcon):
        assert isinstance(bbcon, Bbcon)
        self.bbcon = bbcon
        self.active_behaviors = self.bbcon.active_behaviors

    def choose_action(self):
        pass

