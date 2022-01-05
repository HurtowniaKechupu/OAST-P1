#todo zamienić typ na stringi ["message","server_on","server_off","end"]
class Zdarzenie:
    def __init__(self, typ, t_przyjscia, t_obslugi):
        self.typ = typ
        self.t_przyjscia = t_przyjscia
        self.t_obslugi = t_obslugi
        self.t_wyjscia = 0
        self.next = None


class ListaZdarzen:
    def __init__(self):
        self.head = None

    def print_list(self):
        obecneZdarzenie = self.head
        while obecneZdarzenie is not None:
            print("Typ: {}, Czas przyjścia: {}, Czas obsługi: {}"
                  .format(obecneZdarzenie.typ, obecneZdarzenie.t_przyjscia, obecneZdarzenie.t_obslugi))
            obecneZdarzenie = obecneZdarzenie.next

    def put(self, zdarzenie):
        obecneZdarzenie = self.head
        prev = None
        while obecneZdarzenie is not None:
            if obecneZdarzenie.t_przyjscia > zdarzenie.t_przyjscia:
                if prev is None:
                    NewNode = zdarzenie
                    NewNode.next = self.head
                    self.head = NewNode
                    return
                else:
                    NewNode = zdarzenie
                    NewNode.next = obecneZdarzenie
                    prev.next = NewNode
                    return
            prev = obecneZdarzenie
            obecneZdarzenie = obecneZdarzenie.next
        if self.head is None:
            NewNode = zdarzenie
            NewNode.next = self.head
            self.head = NewNode
            return
        else:
            NewNode = zdarzenie
            prev.next = NewNode
            NewNode.next = None

    def get(self):
        event = self.head
        self.head = self.head.next
        return event

    def isEmpty(self):
        return self.head.next is None
