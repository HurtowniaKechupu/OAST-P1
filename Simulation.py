from Queue1 import *
from System import *


class Simulation:
    def __init__(self, configuration):
        self.configuration = configuration

        self.eventsInSystem = 0
        self.eventsInQueue = 0

        self.timeInSystem = 0.0
        self.timeInQueue = 0.0

        self.meanDelay = 0.0

        self.queue = Queue1()   # pojedyncze zdarzenie generowane w konstruktorze kolejki
        self.system = System(self.queue, self.configuration)    # system (serwer) jest domyślnie pusty

    def run_MM1(self, event_list):
        self.system.updateSystemState()    # stan początkowy systemu
        while not event_list.isEmpty():
            currentEvent = event_list.get()
            self.system.process(currentEvent)   # obsługa zdarzenia

            if currentEvent.type == 0:
                self.queue.put(currentEvent)
                self.system.updateQueueStatistics()

        times = []
        for i in range(len(self.system.processedEvents)):   # obliczenie średniego opóźnienia z uwzględnieniem rozbiegu
            if self.system.processedEvents[i].arrival_time > self.configuration.warmUpTime:
                times.append(self.system.processedEvents[i].out_time - self.system.processedEvents[i].arrival_time)
        self.meanDelay = sum(times) / len(times)

        self.system.updateSystemState()
        return self.meanDelay
