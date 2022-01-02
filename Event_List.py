import Event


class EventList:
    def __init__(self, event_list):
        self.event_list = event_list

    def put(self, type, t_arrival, t_handling, t_next): # rozważyć czy coś samo napłełnia argumenty
        temp = Event.Event(type=type, t_arrival=t_arrival, t_handling=t_handling, t_next=t_next)
        self.event_list.append(temp)

    def get(self):
        temp = self.event_list[0]
        self.event_list.pop(0)
        return temp

    @staticmethod
    def sortuj_liste(list):
        list.sort(key=lambda event: event.t_arrival)