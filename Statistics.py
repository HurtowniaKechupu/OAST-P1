#import matplotlib.pyplot as plt

#todo wywalić statystyki
class Statistics:   # rysowanie wykresu na podstawie zebranych danych
    def __init__(self, configuration):
        self.configuration = configuration

        self.meanDelayInSystemList = []
        self.lambdaList = []
        self.simulationsList = []

    def addStatistics(self, meanDelayInSystem, lambda1):
        self.meanDelayInSystemList.append(meanDelayInSystem)
        self.lambdaList.append(lambda1)

    def plot(self):
        data_sim = []
        data_the = []

        for i in range(len(self.meanDelayInSystemList)):
            data_sim.append((self.lambdaList[i], self.meanDelayInSystemList[i]))

        for i in range(len(self.meanDelayInSystemList)):
            lambda2 = self.lambdaList[i]
            mi = 1 / self.configuration.d

            if self.configuration.switching:
                pOn = self.configuration.econ / (self.configuration.econ + self.configuration.ecoff)
            else:
                pOn = 1

            if self.configuration.switching:
                pOff = self.configuration.ecoff / (self.configuration.econ + self.configuration.ecoff)
            else:
                pOff = 0

            ecoff = self.configuration.ecoff
            ro = lambda2 / (mi * pOn)
            etonoff = (ro + lambda2 * ecoff * pOff) / ((1 - ro) * lambda2)  # E[T] = (lambda /(mu * Pon) + E(Coff) * Poff) / ((1 - lambda / (mu * Pon)) * lambda)
            if etonoff < 1000:
                data_the.append((lambda2, etonoff))

        x_val1 = [a[0] for a in data_sim]
        y_val1 = [a[1] for a in data_sim]
        print(x_val1, y_val1)
        #plt.plot(x_val1, y_val1)
        x_val2 = [b[0] for b in data_the]
        y_val2 = [b[1] for b in data_the]
        print(x_val2, y_val2)
        #plt.plot(x_val2, y_val2)
        #plt.xlabel("Lambda")
        #plt.ylabel("E[T]")
        #plt.legend(['E[T] empiryczne', 'E[T] teoretyczne'])
        #plt.show()
