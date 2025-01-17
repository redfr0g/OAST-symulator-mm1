'''

OAST 2020Z - M/M/1 System Simulator

TODO:
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
import matplotlib.pyplot as plt

# Pobieranie danych
arrv_rate = float(sys.argv[1])
srv_time = float(sys.argv[2])
limit = int(sys.argv[3])

queue = Queue()

empty_system_time = 0
empty_system_prob_dict = {}
system_time = 0
system_time_list = []
service_list = []
clients_in_system_list = []
clients_in_queue_list = []

clients_in_system = 0
clients_in_queue = 0
system_usage = arrv_rate / srv_time

# generowanie czasu pierwszego zgłoszenia i czasu obsługi
next_client = stdrandom.exp(arrv_rate)
next_service = next_client + stdrandom.exp(srv_time)
# obliczenie czasu obługi dla pierwszego kilenta
service_duration = next_service - next_client
service_list.append(service_duration)

server_empty = next_client > next_service

while next_client < limit:

    print(f"Simulation completion: {int(round((next_client / limit) * 100))} %", end='\r')

    while not server_empty:
        queue.enqueue(next_client)
        next_client += stdrandom.exp(arrv_rate)
        server_empty = next_client > next_service
        clients_in_system += 1
        if len(queue) > 1:
            clients_in_queue += 1

    # obsługa pierwszego w kolejce klienta
    current_client = queue.dequeue()
    clients_in_system -= 1
    if len(queue) > 0:
     clients_in_queue -= 1


    # czas przebywania w systemie = czas kiedy klient zostanie obsłużony - czas przybycia klienta
    system_time = next_service - current_client

    if queue.isEmpty():

        # jeżeli kolejka jest pusta, to system obsłuży obecnego klienta szybciej niż nowy napłynie
        # wtedy system będzie pusty do czasu napływu nowego klienta
        empty_system_time += next_client - next_service

        # lista p-stwa pustego systemu w czasie P(t) = czas kiedy system jest pusty/całkowity czas symulacji
        empty_system_prob_dict[next_service] = empty_system_time/next_service

        prev_service_time = next_service
        next_service = next_client + stdrandom.exp(srv_time)
        # jak kolejka jest pusta to czas trawnia obsługi = czas wyjścia - czas przyjścia
        service_duration = next_service - next_client

    else:
        prev_service_time = next_service
        next_service = next_service + stdrandom.exp(srv_time)
        # jak kolejka nie jest pusta to czas trawnia obsługi = czas wyjścia - czas wyjścia poprzedniego klienta
        service_duration = next_service - prev_service_time

    server_empty = next_client > next_service

    # czas przebywania w systemie
    system_time_list.append(system_time)
    # czas obsługi
    service_list.append(service_duration)
    # liczba klientów w systemie
    clients_in_system_list.append(clients_in_system)
    # liczba klientów w kolejce
    clients_in_queue_list.append(clients_in_queue)

mean_system_time = mean(system_time_list)
mean_service = mean(service_list)
mean_clients_in_queue = mean(clients_in_queue_list)
mean_clients_in_system = mean(clients_in_system_list)


print()
print("Mean simulation service time (średni czas obsługi): {}".format(mean_service))
print("Mean theoretical service time (teoretyczny średni czas obsługi): {}".format(1/srv_time))
print()
print("Mean simulation system time (średni czas przebywania w systemie): {}".format(mean_system_time))
print("Mean theoretical system time (teoretyczny średni czas przebywania w systemie): {}".format(1 / (srv_time - arrv_rate)))
print()
print("Mean number of client in a queue (średnia liczba klientów w kolejce): {}".format(mean_clients_in_queue))
print("Mean theoretical number of client in a queue (teoretyczna średnia liczba klientów w kolejce): {}".format((system_usage**2)/(1 - system_usage)))
print()
print("Mean number of client in a system (średnia liczba klientów w systemie): {}".format(mean_clients_in_system))
print("Mean theoretical number of client in a system (teoretyczna średnia liczba klientów w systemie): {}".format(system_usage/(1 - system_usage)))
print()
print("Simulation empty system probability (prawdopodobieństwo pustego systemu): {}".format(empty_system_time/limit))
print("Theoretical empty system probability (teoretyczne prawdopodobieństwo pustego systemu): {}".format(1 - arrv_rate/srv_time))


#Wykres zbieżności prawdopodobieństwa 𝑝0(𝑡) do wartości 𝑝0 z rozkładu stacjonarnego

p0 = 1 - arrv_rate/srv_time
t = empty_system_prob_dict.keys()
p0_vector = [p0] * len(t)
func = empty_system_prob_dict.values()

plt.figure()
plt.plot(t, func, t, p0_vector)
plt.title('Wykres p0(t) do p0 dla ρ={}'.format(arrv_rate/srv_time))
plt.xlabel('Czas symulacji (t)')
plt.ylabel('p0(t)')
plt.ylim(bottom=0, top=1.2)
plt.xlim(left=0, right=limit)

plt.show()

