from motors import Motors

class Motob():
    # gjør om ('L',30) til motorinstruksjoner
    # instruksjoner for venstr og høyre hjul? range[-1,1]

    def __init__(self):
        self.motor = Motors()           # Lager et Motorobjekt?
        self.value = ()                 # Nyligste motor_recommendation sendt hit, ('L',30)
        self.default_svingverdi = 0.5
        self.default_motorverdi = 0.3

    def update(self, tuppel_motorrec_halt_request):
        if tuppel_motorrec_halt_request[1] or tuppel_motorrec_halt_request[0][0] == 'S':    # hvis halt request er true
            self.motor.stop()  # stopper?
            return
        self.value = tuppel_motorrec_halt_request[0]  # setter self.value til motor recommendation
        self.operationalize()  # utfører motor recommendation

    def grader_til_duration(self, grader):
        if grader < 0.01:
            return 0
        return -0.0000786445*grader*grader + 0.0155473*grader - 0.0212085  # ish ok

    def operationalize(self):  # set__value([l,r],duration)
        instruks = self.value[0]
        if instruks == 'L':
            self.motor.set_value([-self.default_svingverdi, self.default_svingverdi], self.grader_til_duration(self.value[1]))
        elif instruks == 'R':
            self.motor.set_value([self.default_svingverdi, -self.default_svingverdi], self.grader_til_duration(self.value[1]))
        elif instruks == 'B':  # eneste andre kommando er forwards, og den vil bare... ja kjøre
            self.motor.set_value([-self.default_motorverdi, -self.default_motorverdi])  # dur = sleep, continue driving
        else:
            self.motor.set_value([self.default_motorverdi, self.default_motorverdi],0.1)
