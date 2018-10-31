from motors import Motors
from arbitrator import Arbitrator

class Motob():
    # gjør om ('L',30) til motorinstruksjoner
    # instruksjoner for venstr og høyre hjul? range[-1,1]

    def __init__(self, arbitrator):
        self.motor = Motors()           # Lager et Motorobjekt?
        self.value = 0                  # Nyligste motor_recommendation sendt hit
        self.arbitrator = arbitrator    # trenger å peke på arbitrator for å oppdatere?

    def update(self):
        t = self.arbitrator.find_optimal_behavior()  # f.eks  (('L',30),False)
        if t[1]:    # hvis halt request er true
            self.motor.stop()  #stopper?
            return
        self.value = t[0]

    def operationalize(self):
        pass



    #360grader på 3 sekunder med fart på 0.5 (av max)
    #120grader på 1 sekund
    #30 grader på 1/4 sekund