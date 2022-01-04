class Queue1:
    def __init__(self):
        self.eventsInQueue = []

    def put(self, event):
        self.eventsInQueue.append(event)

    def get(self):
        if len(self.eventsInQueue) == 0:
            return None
        temp = self.eventsInQueue[0]
        self.eventsInQueue.pop(0)
        return temp

    def size(self):
        return len(self.eventsInQueue)
