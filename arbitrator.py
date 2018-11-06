from bbcon import Bbcon
# tar imot motorforespørsler fra behaviour, og bestemmer hvilke som skal bli utført :)


class Arbitrator:

    def __init__(self, bbcon):
        assert isinstance(bbcon, Bbcon)
        self.bbcon = bbcon  # tar inn bbcon

    def find_optimal_behavior(self):
        largest_weight = 0
        behavior = None  # a behavior object
        for i in range(0, len(self.bbcon.active_behaviors)):                 # for hver behavior i listen i bbcon
            if self.bbcon.active_behaviors[i].weight >= largest_weight:     # sammenlign weights
                behavior = self.bbcon.active_behaviors[i]                       # oppdater viktigste behavior
                largest_weight = self.bbcon.active_behaviors[i].weight          # oppdater vekt
        return behavior                                                     # returnerer behavior

    def choose_action(self):
        winning_behavior = self.find_optimal_behavior()
        motor_rec = winning_behavior.motor_recommendations
        return (motor_rec, winning_behavior.halt_request, winning_behavior)  # (('L',30),False, behavior)
    # motor_recommentaions er en liste med forslag, ett for hvert motorobjekt
