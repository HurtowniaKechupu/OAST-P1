from Configuration import *
from Simulation import *
from Statistics import *

#todo spolszczyć
#todo dodać drukowanie do pliku
def generate_eventList(config1, lambda2):   # generacja listy zdarzeń
    config1.lambda1 = lambda2
    event_list1 = EventList()
    generator = Generator(config1)
    generator.generate(event_list1)
    event_list1.print_list()
    return event_list1


def print_states(x, y, z):
    print("Zmiany stanu systemu (self.currentSystemTime, self.state): {}\n"
          "Zdarzenia w systemie (self.currentSystemTime, self.systemEvent is None ? 0 : 1): {}\n"
          "Zdarzenia w kolejce (self.currentSystemTime, self.eventQueue.size()): {}"
          .format(x, y, z))


task = 1
seed = 128

if task == 1:
    lowerValueOfArrivals = 0.5
    upperValueOfArrivals = 6
    numOfSimulations = 20
    simulationDuration = 500
    switching = False
elif task == 2:
    lowerValueOfArrivals = 0.5
    upperValueOfArrivals = 4
    numOfSimulations = 2
    simulationDuration = 50000
    switching = True
else:
    print("Błedny numer zadania!")
    exit(1)

config = Configuration(lowerValueOfArrivals=lowerValueOfArrivals,
                       upperValueOfArrivals=upperValueOfArrivals,
                       seed=seed,
                       switching=switching,
                       numOfSimulations=numOfSimulations,
                       simulationDuration=simulationDuration,
                       econ=40,
                       ecoff=35,
                       d=0.125,
                       task=task)

print("Symulator kolejki M/M/1 - Zadanie", task)
np.random.seed(config.seed)
statistics = Statistics(config)
lambda1 = config.lowerValueOfArrivals

while lambda1 <= config.upperValueOfArrivals:  # symulacje dla wielu wartości lambda
    meanDelaySystemTimeSum = 0.0  # wartość średniego opóźnienia w systemie E[T]

    print("\nAktualna wartość Lambda:", lambda1)
    for i in range(config.numOfSimulations):  # symulacje powtarzamy wielokrotnie
        event_list = generate_eventList(config, lambda1)
        simulation = Simulation(config)
        meanDelaySim = simulation.run_MM1(event_list)
        meanDelaySystemTimeSum += meanDelaySim
        np.random.seed(config.seed + 10 * i)  # zmiana ziarna po każdej symulacji
        print("Symulacja nr: {}, E[T] w aktualnej symulacji: {}\n".format(i + 1, meanDelaySim))
        print_states(simulation.system.systemState, simulation.system.systemEvents, simulation.system.queueEvents)
        print("------------------------------------------------------------------------------------------------------------------------------------\n")
    print("E[T] dla danej wartości Lambda:", meanDelaySystemTimeSum / config.numOfSimulations)
    statistics.addStatistics(meanDelaySystemTimeSum / config.numOfSimulations, lambda1)
    lambda1 += 0.25

statistics.plot()

