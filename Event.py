class Event:
    def __init__(self, type1, arrival_time, service_time):
        self.type = type1                   # typ: 0 - message; 1 - server_on; 2 - server_off; 3 - end
        self.arrival_time = arrival_time    # czas wejścia - generowany z rozkładem wykładniczym (Poissona)
        self.service_time = service_time    # czas obsługi - generowany z rozkładem wykładniczym (Poissona)
        self.out_time = 0                   # czas wyjścia - rzeczywisty czas wyjścia; out_time != arrival_time + service_time

        self.next = None


class EventList:    # w formie listy jednokierunkowej (single linked list)
    def __init__(self):
        self.head = None

    def print_list(self):
        curr = self.head
        while curr is not None:
            print("Typ: {}, Czas przybycia: {}, Czas obsługi: {}"
                  .format(curr.type, curr.arrival_time, curr.service_time))
            curr = curr.next

    def put(self, event):
        curr = self.head
        prev = None
        while curr is not None:
            if curr.arrival_time > event.arrival_time:
                if prev is None:
                    NewNode = event
                    NewNode.next = self.head
                    self.head = NewNode
                    return
                else:
                    NewNode = event
                    NewNode.next = curr
                    prev.next = NewNode
                    return
            prev = curr
            curr = curr.next
        if self.head is None:
            NewNode = event
            NewNode.next = self.head
            self.head = NewNode
            return
        else:
            NewNode = event
            prev.next = NewNode
            NewNode.next = None

    def get(self):
        event = self.head
        self.head = self.head.next
        return event

    def isEmpty(self):
        return self.head.next is None
