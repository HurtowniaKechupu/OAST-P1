import numpy as np


class Poisson:  # generator Poissona
    def __init__(self, configuration):
        self.configuration = configuration

    @staticmethod
    def generateRandomEventWithMean(mean):
        return -np.log(1 - np.random.random()) / mean
