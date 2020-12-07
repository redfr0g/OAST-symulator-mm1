'''

OAST 2020Z - M/M/1 "continuous service" System Simulator - part II

Usage:
C:\>python mm1_continuous_service.py <Arrival rate> <Service rate> <Simulation limit>

Example:
C:\>python mm1_continuous_service.py .1 .4 1000

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

ρ = arrv_rate/srv_time

empty_system_time = 0
empty_system_prob_dict = {}
wait_list = []
service_list = []
n_system_list = []
n_queue_list = []

n_system = 0
n_queue = 0

next_arrival = stdrandom.exp(arrv_rate)
next_service = next_arrival + stdrandom.exp(srv_time)
#obliczenie czasu obługi dla pierwszego kilenta
service_duration = next_service - next_arrival
service_list.append(service_duration)



while next_arrival < limit:

    print(f"Simulation completion: {int(round((next_arrival/limit)*100))} %", end='\r')

    #sprawdzamy czy następnym zdarzeniem jest obługa czy zgłoszenie; jeżeli zgłoszenie to dodajemy nowe zgłoszenie do kolejki
    while next_arrival < next_service:
        queue.enqueue(next_arrival)
        n_system += 1
        next_arrival += stdrandom.exp(arrv_rate)



    #arrival - to klient, którego teraz będziemy obłsugiwać
    #sprawdzamy czy obsługujemy prawdziwego czy wyimaginowanego klienta, jak wyimaginowanego to kolejka może być pusta
    #być może będziemy obługiwać kliku wyimaginowanych klietnów przy długich odstępach pomiędzy zgłoszeniami
    if not queue.isEmpty():
        arrival = queue.dequeue()
        n_system -= 1
        #czas przebywania w systemie = czas kiedy klient zostanie obsłużony - czas przybycia klienta
        wait_time = next_service - arrival

    if queue.isEmpty():

        prev_service_time = next_service

        # jeżeli kolejka jest pusta i system obsłuży klienta szybciej niż nowy napłynie to wtedy system będzie pusty do czasu napływu nowego klienta
        if next_service < next_arrival:
            empty_system_time += next_arrival - next_service

            # lista p-stwa pustego systemu w czasie P(t) = czas kiedy system jest pusty/całkowity czas symulacji
            empty_system_prob_dict[next_service] = empty_system_time/next_service

            #w tej stytuacji zabieramy się za wyimaginowanego klienta
            next_service = next_service + stdrandom.exp(srv_time)
        else:
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
    n_system_list.append(n_system)

mean_wait = mean(wait_list)
mean_service = mean(service_list)
mean_n_system = mean(n_system_list)


#zakomentowalam i moim zdaniem to jest do usunięcia to bo my tutaj nigdzie nie obliczamy średniego czasu przebywania w kolejce
#mean_system = mean_wait + mean_service



print()
print("Teoretyczna średnia liczba klientów w buforze E[Q]: {}".format(ρ/(1-ρ) ))
print()
print("Teoretyczna średnia liczba klientów w systemie E[N]: {}".format(((2-ρ)*ρ)/(1-ρ)))
print()
print("Teoretyczny średni czas oczekiwania na obsługę E[W]: {}".format( ρ/(arrv_rate*(1-ρ)) ))
print()
print("Teoretyczny średni czas przejścia przez system E[T]: {}".format( ((2-ρ)*ρ)/(arrv_rate*(1-ρ)) ))

print("Teoretyczny średni czas przejścia przez system E[N]: {}".format(mean_n_system))

