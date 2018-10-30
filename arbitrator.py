from bbcon import Bbcon
import random
#tar imot motorforespørsler fra behaviour, og bestemmer hvilke som skal bli utført :)

class Arbitrator():

    def __init__(self, bbcon):
        self.bbcon = bbcon

    def find_optimal_behavior(self):
        largest_weight = 0
        behavior = None  # a behavior object
        # redd for at det ikke går å iterere over behavior, siden det ikke er noen definert iterator for klassen?
        for i in range(0,len(self.bbcon.active_behaviors)):                 # for hver behavior i listen i bbcon
            if self.bbcon.active_behaviors[i].weigth >= largest_weight:     # sammenlign weights
                behavior = self.bbcon.active_behaviors[i]                       # oppdater viktigste behavior
                largest_weight = self.bbcon.active_behaviors[i].weight          # oppdater vekt
        return behavior                                                      # returnerer behavior

    def choose_action(self):
        best_behavior, largest_weight = self.find_optimal_behavior()
        motor_rec = best_behavior.motor_recommendations


