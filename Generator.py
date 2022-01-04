from Event import *
import numpy as np


class Poisson:  # generator Poissona
    def __init__(self, configuration):
        self.configuration = configuration

    @staticmethod
    def generateRandomEventWithMean(mean):
        return -np.log(1 - np.random.random()) / mean


class Generator(Poisson):
    def __init__(self, configuration):
        super().__init__(configuration)

    def getMessageTimeGenerator(self):
        return self.generateRandomEventWithMean(self.configuration.lambda1)

    def generate(self, event_list1):
        self.generateMessages(event_list1)
        if self.configuration.switching:
            self.generateSwitchingEvents(event_list1)

        e = Event(3, self.configuration.simulationDuration, 0)  # na końcu generowane zdarzenie typu 3 - koniec
        event_list1.put(e)
        return event_list1

    def generateMessages(self, event_list):     # generator zdarzeń typu 0
        time = self.getMessageTimeGenerator()
        if self.configuration.numberOfMessages:
            number_of_messages = self.configuration.numberOfMessages
            while number_of_messages != 0:
                e = Event(0, time, self.generateRandomEventWithMean(1 / self.configuration.d))
                event_list.put(e)

                time += self.getMessageTimeGenerator()
                number_of_messages -= 1

            while time < self.configuration.simulationDuration:
                e = Event(0, time, self.generateRandomEventWithMean(1 / self.configuration.d))
                event_list.put(e)

                time += self.getMessageTimeGenerator()

    def generateSwitchingEvents(self, event_list):  # generator zdarzeń typu 1 i 2
        time = self.generateRandomEventWithMean(1/self.configuration.econ)
        isOn = True
        while time < self.configuration.simulationDuration:
            if isOn:
                e = Event(2, time, 0)
                time += self.generateRandomEventWithMean(1/self.configuration.ecoff)
                isOn = False
            else:
                e = Event(1, time, 0)
                time += self.generateRandomEventWithMean(1 / self.configuration.econ)
                isOn = True

            event_list.put(e)
