'''

OAST 2020Z - M/M/1 System Simulator

TODO:
- add code comments
- optimalisation
- add empty system probability distribution graph
- add continous service model
- add cmd input with flags

Usage:
C:\>python mm1_sim.py <Arrival rate> <Service rate> <Simulation limit>

Example:
C:\>python mm1_sim.py .1 .4 1000

'''
import sys
import stdrandom
from linkedqueue import Queue
from statistics import mean

# Pobieranie danych
arrv_rate = float(sys.argv[1])
srv_time = float(sys.argv[2])
limit = int(sys.argv[3])

# Calculate theoretical mean time spent in system
mean_system_theo = 1 / (srv_time * (1 - arrv_rate / srv_time))

queue = Queue()

prev_wait_time = 0
wait_list = []
service_list = []

next_arrival = stdrandom.exp(arrv_rate)
next_service = next_arrival + stdrandom.exp(srv_time)

while next_arrival < limit:

    print(f"Simulation completion: {int(round((next_arrival/limit)*100))} %", end='\r')

    while next_arrival < next_service:
        queue.enqueue(next_arrival)
        next_arrival += stdrandom.exp(arrv_rate)

#obsługa nowego pakietu
    arrival = queue.dequeue()
#czas przebywania w systemie = czas kiedy klient zostanie obsłużony - czas przybycia klienta
    wait_time = next_service - arrival

#czas obsługi w serwerze = cały czas w systemie - czas wyjścia poprzedniego klienta
    wait_duration = wait_time - prev_wait_time
    prev_wait_time = wait_time

    if queue.isEmpty():
        prev_service_time = next_service
        next_service = next_arrival + stdrandom.exp(srv_time)
#jak kolejka jest pusta to czas trawnia obsługi = czas wyjścia - czas przyjścia
        service_duration = next_service - next_arrival
    else:
        prev_service_time = next_service
        next_service = next_service + stdrandom.exp(srv_time)
# jak kolejka nie jest pusta to czas trawnia obsługi = czas wyjścia - czas wyjścia poprzedniego klienta
        service_duration = next_service - prev_service_time

#średni czas przebywania w systemie
    wait_list.append(wait_time)
#średni czas obsługi
    service_list.append(service_duration)

mean_wait = mean(wait_list)
mean_service = mean(service_list)

#zakomentowalam i moim zdaniem to jest do usunięcia to bo my tutaj nigdzie nie obliczamy średniego czasu przebywania w kolejce
#mean_system = mean_wait + mean_service

print()
#print("Mean simulation queue wait time: {}".format(mean_wait))
print("Mean simulation service time(średni czas obsługi): {}".format(mean_service))
print("Mean simulation system time (średni czas przebywania w systemie): {}".format(mean_wait))

print("Mean theoretical system time (teoretyczny średni czas obsługi): {}".format(1/srv_time))
print("Mean theoretical system time (teoretyczny średni czas przebywania w systemie): {}".format(mean_system_theo))

