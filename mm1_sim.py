'''

OAST 2020Z - M/M/1 System Simulator

TODO:
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
import matplotlib.pyplot as plt

# Pobieranie danych
arrv_rate = float(sys.argv[1])
srv_time = float(sys.argv[2])
limit = int(sys.argv[3])

# Calculate theoretical mean time spent in system
#mean_system_time_theory = 1 / (srv_time * (1 - arrv_rate / srv_time))
mean_system_time_theory = 1 / (srv_time - arrv_rate)

queue = Queue()

#prev_wait_time = 0
empty_system_time = 0
empty_system_prob_dict = {}
wait_list = []
service_list = []
n_system_list = []
n_queue_list = []

n_system = 0
n_queue = 0
ρ = arrv_rate/srv_time

next_arrival = stdrandom.exp(arrv_rate)
next_service = next_arrival + stdrandom.exp(srv_time)
#obliczenie czasu obługi dla pierwszego kilenta
service_duration = next_service - next_arrival
service_list.append(service_duration)



while next_arrival < limit:

    print(f"Simulation completion: {int(round((next_arrival/limit)*100))} %", end='\r')

    while next_arrival < next_service:
        queue.enqueue(next_arrival)
        n_system += 1
        next_arrival += stdrandom.exp(arrv_rate)


    #obsługa nowego pakietu
    arrival = queue.dequeue()

    #czas przebywania w systemie = czas kiedy klient zostanie obsłużony - czas przybycia klienta
    #arrival - to klient, którego teraz będziemy obłsugiwać
    wait_time = next_service - arrival

    #czas obsługi w serwerze = cały czas w systemie - czas wyjścia poprzedniego klienta
    #wait_duration = wait_time - prev_wait_time
    #prev_wait_time = wait_time

    if queue.isEmpty():

        # jeżeli kolejka jest pusta i system obsłuży klienta szybciej niż nowy napłynie to wtedy system będzie pusty do czasu napływu nowego klienta
        if next_service < next_arrival:
            empty_system_time += next_arrival - next_service

            # lista p-stwa pustego systemu w czasie P(t) = czas kiedy system jest pusty/całkowity czas symulacji
            empty_system_prob_dict[next_service] = empty_system_time/next_service

        prev_service_time = next_service
        next_service = next_arrival + stdrandom.exp(srv_time)
        #jak kolejka jest pusta to czas trawnia obsługi = czas wyjścia - czas przyjścia
        service_duration = next_service - next_arrival
        n_system -= 1

    else:
        prev_service_time = next_service
        next_service = next_service + stdrandom.exp(srv_time)
        # jak kolejka nie jest pusta to czas trawnia obsługi = czas wyjścia - czas wyjścia poprzedniego klienta
        service_duration = next_service - prev_service_time
        n_system -= 1

    # średni czas przebywania w systemie
    wait_list.append(wait_time)
    # średni czas obsługi
    service_list.append(service_duration)
    # średnia liczba klientów w systemie
    n_system_list.append(n_system)
    # średnia liczba klientów w kolejce - DO POPRAWY
    n_queue_list.append(len(queue))


mean_wait = mean(wait_list)
mean_service = mean(service_list)
mean_n_queue = mean(n_queue_list)
mean_n_system = mean(n_system_list)


#zakomentowalam i moim zdaniem to jest do usunięcia to bo my tutaj nigdzie nie obliczamy średniego czasu przebywania w kolejce
#mean_system = mean_wait + mean_service

print()
#print("Mean simulation queue wait time: {}".format(mean_wait))
print("Mean simulation service time (średni czas obsługi): {}".format(mean_service))
print("Mean theoretical system time (teoretyczny średni czas obsługi): {}".format(1/srv_time))
print()
print("Mean simulation system time (średni czas przebywania w systemie): {}".format(mean_wait))
print("Mean theoretical system time (teoretyczny średni czas przebywania w systemie): {}".format(mean_system_time_theory))
print()
print("Mean number of client in a queue (średnia liczba klientów w kolejce): {}".format(mean_n_queue))
print("Mean theoretical number of client in a queue 1 (teoretyczna średnia liczba klientów w kolejce): {}".format(arrv_rate*(ρ/(srv_time-arrv_rate))))
print("Mean theoretical number of client in a queue 2 (teoretyczna średnia liczba klientów w kolejce): {}".format((ρ*ρ)/(1-ρ)))
print()
print("Mean number of client in a system (średnia liczba klientów w systemie): {}".format(mean_n_system))
print("Mean theoretical number of client in a system (teoretyczna średnia liczba klientów w systemie): {}".format(arrv_rate/(srv_time-arrv_rate)))
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

