'''

OAST 2020Z - M/M/1 System Simulator

TODO:
- add cmd input with flags
- test calculations with constant imaginary client service time (equal to mean real client service time)

Usage:
C:\>python mm1_continous_service.py <Arrival rate> <Service rate> <Simulation limit>

Example:
C:\>python mm1_continous_service.py .1 .4 1000

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
#mean_system_time_theory = 1 / (srv_time * (1 - arrv_rate / srv_time))
mean_system_time_theory = 1 / (srv_time - arrv_rate)

queue = Queue()

imaginary_service_time = 0
imaginary_client_prob_list = []
wait_list = []
service_list = []
queue_time_list = []
clients_in_system_list = []
clients_in_queue_list = []

clients_in_system = 0
clients_in_queue = 0
system_usage = arrv_rate / srv_time

next_arrival = stdrandom.exp(arrv_rate)
next_service = next_arrival + stdrandom.exp(srv_time)

#obliczenie czasu obługi dla pierwszego kilenta
service_duration = next_service - next_arrival
service_list.append(service_duration)

while next_arrival < limit:

    print(f"Simulation completion: {int(round((next_arrival/limit)*100))} %", end='\r')

    while next_arrival < next_service:
        queue.enqueue(next_arrival)
        clients_in_system += 1
        clients_in_queue += 1
        next_arrival += stdrandom.exp(arrv_rate)

    #obsługa nowego pakietu
    if clients_in_queue == 0:
        pass
    else:
        arrival = queue.dequeue()
        clients_in_queue -= 1
        clients_in_system -= 1

    #czas przebywania w systemie = czas kiedy klient zostanie obsłużony - czas przybycia klienta
    #arrival - to klient, którego teraz będziemy obłsugiwać
        wait_time = next_service - arrival

    #czas obsługi w serwerze = cały czas w systemie - czas wyjścia poprzedniego klienta
    #wait_duration = wait_time - prev_wait_time
    #prev_wait_time = wait_time

    if queue.isEmpty():

        # dla pewności że nie będze błędu przy pustej kolejce
        clients_in_queue = 0

        # jeżeli kolejka jest pusta i system obsłuży klienta szybciej niż nowy napłynie to wtedy system będzie pusty do czasu napływu nowego klienta
        if next_service < next_arrival:
            clients_in_system = 1
            prev_service_time = next_service
            # Continous Service - obsługujemy od razu wyimaginowanego klienta
            next_service = next_service + stdrandom.exp(srv_time)
            # czas trawnia obsługi = czas wyjścia - czas przyjścia
            service_duration = next_service - prev_service_time
            imaginary_service_time += service_duration

        else:
            clients_in_system = 1
            prev_service_time = next_service
            next_service = next_arrival + stdrandom.exp(srv_time)
            # jak kolejka jest pusta to czas trawnia obsługi = czas wyjścia - czas przyjścia
            service_duration = next_service - next_arrival

    else:
        prev_service_time = next_service
        next_service = next_service + stdrandom.exp(srv_time)
        # jak kolejka nie jest pusta to czas trawnia obsługi = czas wyjścia - czas wyjścia poprzedniego klienta
        service_duration = next_service - prev_service_time

    # średni czas przebywania w systemie
    wait_list.append(wait_time)
    # średni czas obsługi
    service_list.append(service_duration)
    # średniczas w kolejce
    queue_time_list.append(wait_time - service_duration)
    # średnia liczba klientów w systemie
    clients_in_system_list.append(clients_in_system)
    # średnia liczba klientów w kolejce - DO POPRAWY
    clients_in_queue_list.append(clients_in_queue)


mean_wait = mean(wait_list)
mean_service = mean(service_list)
mean_queue = mean(queue_time_list)
mean_clients_in_queue = mean(clients_in_queue_list)
mean_clients_in_system = mean(clients_in_system_list)
mean_imaginary_client_prob = imaginary_service_time/limit
#zakomentowalam i moim zdaniem to jest do usunięcia to bo my tutaj nigdzie nie obliczamy średniego czasu przebywania w kolejce
#mean_system = mean_wait + mean_service

print()
print("Teoretyczna średnia liczba klientów w kolejce E[Q]: {}".format(system_usage / (1 - system_usage)))
print("Symulacyjna średnia liczba klientów w kolejce E[Q]: {}".format(mean_clients_in_queue))
print()
print("Teoretyczna średnia liczba klientów w systemie E[N]: {}".format(((2 - system_usage) * system_usage) / (1 - system_usage)))
print("Symulacyjna średnia liczba klientów w systemie E[N]: {}".format(mean_clients_in_system))
print()
print("Teoretyczny średni czas oczekiwania na obsługę E[W]: {}".format(system_usage / (arrv_rate * (1 - system_usage))))
print("Symulacyjny średni czas oczekiwania na obsługę E[W]: {}".format(mean_queue))
print()
print("Teoretyczny średni czas przejścia przez system E[T]: {}".format(((2 - system_usage) * system_usage) / (arrv_rate * (1 - system_usage))))
print("Symulacyjny średni czas przejścia przez system E[T]: {}".format(mean_wait))
print()
print("Symulacyjne prawdopodobienstwo obsługi wyimaginowanego klienta Pimg: {}".format(mean_imaginary_client_prob))
