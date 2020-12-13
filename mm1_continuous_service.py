'''

OAST 2020Z - M/M/1 System Simulator

TODO:
- add cmd input with flags
- test calculations with constant imaginary client service time (equal to mean real client service time)

Usage:
C:\>python mm1_continuous_service.py <Arrival rate> <Service rate> <Simulation limit>

Example (random imaginary service time):
C:\>python mm1_continuous_service.py .1 .4 1000

Example (static imaginary service time):
C:\>python mm1_continuous_service.py .1 .4 1000 static

'''
import sys
import stdrandom
from linkedqueue import Queue
from statistics import mean

print(len(sys.argv))
# Pobieranie danych
if len(sys.argv) == 4:
    arrv_rate = float(sys.argv[1])
    srv_time = float(sys.argv[2])
    limit = int(sys.argv[3])
    img_service_type = "random"
else:
    arrv_rate = float(sys.argv[1])
    srv_time = float(sys.argv[2])
    limit = int(sys.argv[3])
    # do użycia w przypadku stałego czasu obsługi klientów wyimaginowanych
    img_service_type = str(sys.argv[4])

queue = Queue()

imaginary_service_time = 0
imaginary_client_prob_list = []
system_time_list = []
service_list = []
queue_time_list = []
clients_in_system_list = []
clients_in_queue_list = []

clients_in_system = 0
clients_in_queue = 0
system_usage = arrv_rate / srv_time
flag = 0

next_client = stdrandom.exp(arrv_rate)
next_service = next_client + stdrandom.exp(srv_time)
# obliczenie czasu obługi dla pierwszego kilenta
service_duration = next_service - next_client

mean_service = 1/arrv_rate
service_list.append(service_duration)

server_empty = next_client > next_service

real_client = True


while next_client < limit:

    print(f"Simulation completion: {int(round((next_client / limit) * 100))} %", end='\r')

    while not server_empty:
        queue.enqueue(next_client)
        next_client += stdrandom.exp(arrv_rate)
        server_empty = next_client > next_service
        clients_in_system += 1
        if len(queue) > 1:
            clients_in_queue += 1


    # sprawdzamy czy w systemie jest jakiś klient, czy będzie obsługiwany klient wyimaginowany
    if not queue.isEmpty():
        current_client = queue.dequeue()
        if len(queue) > 0:
            clients_in_queue -= 1
        clients_in_system -= 1
        # czas przebywania w systemie = czas kiedy klient zostanie obsłużony - czas przybycia klienta
        system_time = next_service - current_client
        real_client = True

    if queue.isEmpty():

        prev_service_time = next_service

        # jeżeli kolejka jest pusta i system obsłuży klienta szybciej niż nowy napłynie to wtedy system ma obsłużyć
        # wyimaginowanego klienta
        if next_service < next_client:

            # Continous Service - obsługujemy od razu wyimaginowanego klienta
            if img_service_type == "static":
                next_service = next_service + mean_service
            else:
                next_service = next_service + stdrandom.exp(srv_time)

            #service_duration = next_service - prev_service_time
            imaginary_service_time += service_duration
            real_client = False
        else:
            flag += 1
            next_service = next_client + stdrandom.exp(srv_time)
            # (klienci prawdziwi) jak kolejka jest pusta to czas trawnia obsługi = czas wyjścia - czas przyjścia
            service_duration = next_service - next_client

    else:
        prev_service_time = next_service
        next_service = next_service + stdrandom.exp(srv_time)
        # (klienci prawdziwi) jak kolejka nie jest pusta to czas trawnia obsługi = czas wyjścia - czas wyjścia poprzedniego klienta
        service_duration = next_service - prev_service_time

    server_empty = next_client > next_service

    if real_client:
        # średni czas przebywania w systemie prawdziwych klientów
        system_time_list.append(system_time)
        # średni czas obsługi prawdziwych klientów
        service_list.append(service_duration)
        # średni czas przebywania w kolejce prawdziwych klientów
        queue_time_list.append(system_time - service_duration)
        # średnia liczba prawdziwych klientów w systemie
        clients_in_system_list.append(clients_in_system)
        # średnia liczba prawdziwych klientów w kolejce
        clients_in_queue_list.append(clients_in_queue)


mean_service = mean(service_list)
mean_system_time = mean(system_time_list)
mean_queue = mean(queue_time_list)
mean_clients_in_queue = mean(clients_in_queue_list)
mean_clients_in_system = mean(clients_in_system_list)
mean_imaginary_client_prob = imaginary_service_time/limit


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
print("Symulacyjny średni czas przejścia przez system E[T]: {}".format(mean_system_time))
print()
print("Symulacyjne prawdopodobienstwo obsługi wyimaginowanego klienta Pimg: {}".format(mean_imaginary_client_prob))
print(flag)
