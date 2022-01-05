
#todo spolszczyć
<<<<<<< HEAD:Kolejka.py
class Kolejka:
=======
class Queue:
>>>>>>> 5f44afbee02f09b65a99e0c53929d1bbf75defc1:Queue.py
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
