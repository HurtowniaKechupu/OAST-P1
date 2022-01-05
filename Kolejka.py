class Kolejka:
    def __init__(self):
        self.zdarzeniaWKolejce = []

    def put(self, event):
        self.zdarzeniaWKolejce.append(event)

    def get(self):
        if len(self.zdarzeniaWKolejce) == 0:
            return None
        temp = self.zdarzeniaWKolejce[0]
        self.zdarzeniaWKolejce.pop(0)
        return temp

    def size(self):
        return len(self.zdarzeniaWKolejce)
