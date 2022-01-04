from Poisson import *


class System(Poisson):
    def __init__(self, queue, configuration):
        super().__init__(configuration)
        self.eventQueue = queue

        self.currentTime = 0.0
        self.currentSystemTime = 0.0
        self.state = 1
        self.timeOff = 0.0
        self.timeOn = 0.0

        self.systemEvent = None
        self.remainingProcessingTime = 0.0
        self.timeIdle = 0.0
        self.timeProcessing = 0.0

        self.processedEvents = []
        self.queueEvents = []
        self.systemEvents = []
        self.systemState = []

    def process(self, current_event):
        self.currentTime = current_event.arrival_time
        self.doProcessing()
        self.currentSystemTime = self.currentTime

        if current_event.type == 1:     # obsługa włączeń i wyłączeń serwera
            self.state = 1
            self.updateSystemState()
        elif current_event.type == 2:
            self.state = 2
            self.updateSystemState()

    def doProcessing(self):
        timePassed = self.currentTime - self.currentSystemTime
        if self.state == 2:
            self.timeOff += timePassed
            return
        else:
            self.timeOn += timePassed

        while self.currentSystemTime < self.currentTime:    # obsługa zdarzenia
            self.processEvent()

    def processEvent(self):
        if self.systemEvent is None:
            self.systemEvent = self.eventQueue.get()
            if self.systemEvent is not None:
                self.remainingProcessingTime = self.systemEvent.service_time

            self.updateSystemEvents()
            self.updateQueueStatistics()

        if self.systemEvent is None:    # jeśli zdarzenie jest null, tzn. że kolejka jest pusta i nic się nie wydarzyło
            self.timeIdle += self.currentTime - self.currentSystemTime
            self.currentSystemTime = self.currentTime
            self.updateSystemEvents()
            return

        self.currentSystemTime += self.remainingProcessingTime

        if self.currentSystemTime < self.currentTime:   # zdarzenie obsłużone
            self.systemEvent.out_time = self.currentSystemTime
            self.processedEvents.append(self.systemEvent)
            self.systemEvent = None
            self.timeProcessing += self.remainingProcessingTime
        else:   # zdarzenie częściowo obsłużone
            self.timeProcessing += (self.remainingProcessingTime - (self.currentSystemTime - self.currentTime))
            self.remainingProcessingTime = self.currentSystemTime - self.currentTime
            self.currentSystemTime = self.currentTime

    def updateQueueStatistics(self):        # jeśli size się zwiększa tzn. że do kolejki wchodzi zdarzenia; jeśli size się zmniejsza tzn. że z kolejki wychodzi zdarzenie
        self.queueEvents.append((self.currentSystemTime, self.eventQueue.size()))

    def updateSystemState(self):            # jeśli state 1 - włączenie systemu; jeśli state 2 - wyłączenie systemu
        self.systemState.append((self.currentSystemTime, self.state))

    def updateSystemEvents(self):           # brak uaktualnień kiedy system jest OFF
        if self.systemEvent is None:
            x = 0
        else:
            x = 1
        self.systemEvents.append((self.currentSystemTime, x))
