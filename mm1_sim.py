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
        next_arrival += stdrandom.exp(srv_time)

    arrival = queue.dequeue()
    wait_time = next_service - arrival

    wait_duration = wait_time - prev_wait_time
    prev_wait_time = wait_time

    if queue.isEmpty():
        prev_service_time = next_service
        next_service = next_arrival + stdrandom.exp(srv_time)
        service_duration = next_service - prev_service_time
    else:
        prev_service_time = next_service
        next_service = next_service + stdrandom.exp(srv_time)
        service_duration = next_service - prev_service_time

    wait_list.append(wait_duration)
    service_list.append(service_duration)

mean_wait = mean(wait_list)
mean_service = mean(service_list)
mean_system = mean_wait + mean_service

print()
print("Mean simulation queue wait time: {}".format(mean_wait))
print("Mean simulation service time: {}".format(mean_service))
print("Mean simulation system time: {}".format(mean_system))

print("Mean theoretical system time: {}".format(mean_system_theo))
