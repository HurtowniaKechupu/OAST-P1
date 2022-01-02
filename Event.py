class Event(object):

    def __init__(self, type, t_arrival, t_handling, t_next):
        self.type = type
        self.t_arrival = t_arrival
        self.t_handling = t_handling
        self.t_next = t_next
        # rozważyć cyz nie dać self.t_prev = t_prev