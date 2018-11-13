from abc import abstractmethod


class Behavior(): #abstract class

    def __init__(self, bbcon):
        self.bbcon = bbcon                        #peker til bbcon objektet
        self.motor_recommendations = ('F', )      #Inneholder senest oppdatert motor recommendations
        self.active_flag = False                  #forteller om metoden er aktiv
        self.halt_request = False                 #avslutte oppførelse totalt
        self.match_degree = 0                     #hvor viktig oppførselen er akkurat nå, regnes ut i metoden fra sensor verdier
        self.weight = 0                           #self.priority * self.match_degree #sendes til Arbitrator, som indikere hvor viktig metoden er totaltsett

    @abstractmethod
    def consider_deactivation(self):      #Setter self.active_flag = False, kaller metoder i bbcon for å skru av/på kamera/refleksjonssensor
        pass

    @abstractmethod
    def consider_activation(self):        #Setter self.active_flag = True, kaller metoder i bbcon for å skru av/på kamera/refleksjonssensor
        pass

    @abstractmethod
    def update(self):                     #kaller sensobs update funksjon for å oppdatere verdier, kaller sense_and_act() og regner ut self.weight
        pass

    @abstractmethod
    def sense_and_act(self):              #legger inn motor recommendations og gir self.match_degree en variabel
        pass

    @abstractmethod
    def reset_sensob(self):
        pass


class DontCrash(Behavior):

    def __init__(self, bbcon, ultrasonicsensob):
        super(DontCrash, self).__init__(bbcon)
        self.sensob = ultrasonicsensob
        self.active_flag = True
        self.dist = None                     #distansen er i cm
        self.priority = 1

    # kaller sensobs update funksjon for å oppdatere verdier, kaller sense_and_act() og regner ut self.weight
    def update(self):
        self.dist = self.sensob.update()     #distansen er i cm
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    #Setter self.active_flag = False, kaller metoder i bbcon for å skru av/på kamera/refleksjonssensor
    def consider_deactivation(self):
        pass

    # Setter self.active_flag = True, kaller metoder i bbcon for å skru av/på kamera/refleksjonssensor
    def consider_activation(self):
        pass

    # legger inn motor recommendations og gir self.match_degree en variabel
    def sense_and_act(self):
        if self.active_flag:
            if self.dist > 20:                          #hvis distansen er større enn 20 cm er metdoen urelevant
                self.match_degree = 0
                self.motor_recommendations = ('F',)
            elif self.dist <= 5:                        #metode veldig relevant
                self.match_degree = 1
                self.motor_recommendations = ('R', 180)
            else:                                       #metode middels relevant
                self.match_degree = 1-((self.dist-5)/20)
                self.motor_recommendations = ('R', 180)

    # kaller sensobs reset metode
    def reset_sensob(self):
        self.sensob.reset()


class FollowLine(Behavior):

    def __init__(self, bbcon, reflectancesensob):
        super(FollowLine, self).__init__(bbcon)
        self.sensob = reflectancesensob
        self.active_flag = False
        self.reflectvalues = None
        self.priority = 0.5

    # kaller sensobs update funksjon for å oppdatere verdier, kaller sense_and_act() og regner ut self.weight
    def update(self):
        self.reflectvalues = self.sensob.update()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

        print('Update FollowLine:')
        print('Values:', self.reflectvalues)
        print('Recomendation:', self.motor_recommendations, '\n')

    # legger inn motor recommendations og gir self.match_degree en variabel
    def sense_and_act(self, threshold = 0.05):
        if self.active_flag:
            degrees = {0:20, 1:7, 2:0, 3:0, 4:7, 5:20}
            maxval = 0  # maximum value
            index = 0  # index of maxval
            for i in range(len(self.reflectvalues)):  # find maxval and index of maxval in array
                self.reflectvalues[i] = 1 - self.reflectvalues[i]
                if self.reflectvalues[i] > maxval:
                    maxval = self.reflectvalues[i]
                    index = i
            if maxval < threshold:
                self.motor_recommendations = ('L, 45')
                self.match_degree = 0
            else:
                direction = 'R' if index > 3 else 'L'
                if degrees[index] == 0:
                    self.motor_recommendations = ('F',)
                self.motor_recommendations = (direction, degrees[index])
                self.match_degree = 1

    # Setter self.active_flag = True, kaller metoder i bbcon for å skru av/på kamera/refleksjonssensor
    def consider_activation(self):
        if self.bbcon.should_follow_line():
            self.active_flag = True

    # Setter self.active_flag = False, kaller metoder i bbcon for å skru av/på kamera/refleksjonssensor
    def consider_deactivation(self):
        if not self.bbcon.should_follow_line():
            self.active_flag = False

    # kaller sensobs reset metode
    def reset_sensob(self):
        self.sensob.reset()


class FindColoredObject(Behavior):
    
    def __init__(self, bbcon, camerasensob):
        super(FindColoredObject, self).__init__(bbcon)
        self.sensob = camerasensob
        self.active_flag = False
        self.array = None
        self.priority = 0.8

    #kaller sensobs update funksjon for å oppdatere verdier, kaller sense_and_act() og regner ut self.weight
    def update(self):
        self.array = self.sensob.update()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    # legger inn motor recommendations og gir self.match_degree en variabel
    def sense_and_act(self, threshold=0.05):
        if self.active_flag:
            maxval = 0  # maximum value
            index = 0  # index of maxval
            for i in range(len(self.array)):  # find maxval and index of maxval in array
                if self.array[i] > maxval:
                    maxval = self.array[i]
                    index = i
            if maxval < threshold:
                self.motor_recommendations = ('L, 60')
                self.match_degree = 0
            else:
                direction = 'R' if index > 3 else 'L'
                degree = {0: 32, 1: 16, 2: 8, 3: 0, 4: 0, 5: 8, 6: 16, 7: 32}
                self.motor_recommendations = (direction, degree[index])
                if degree[index] == 0:
                    self.motor_recommendations = ('F',)
                self.match_degree = 1

    # Setter self.active_flag = False, kaller metoder i bbcon for å skru av/på kamera/refleksjonssensor
    def consider_deactivation(self):
        if not self.bbcon.should_camera_be_on():
            self.active_flag = True

    # Setter self.active_flag = True, kaller metoder i bbcon for å skru av/på kamera/refleksjonssensor
    def consider_activation(self):
        if self.bbcon.should_camera_be_on():
            self.active_flag = False

    # kaller sensobs reset metode
    def reset_sensob(self):
        self.sensob.reset()
