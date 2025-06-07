from queue import Queue
from random import expovariate
from enum import Enum

class QueueSimulator:

    # -----------------------------
    # Constants
    # -----------------------------

    SIMULATION_TIME = int(2e4)  # in minutes
    MU = 12                     # minutely rate
    LAMDA = 6                   # minutely rate

    class QueueEvent(Enum):
        ARRIVAL = 0,
        DEPARTURE = 1


    # -----------------------------
    # Constructor
    # -----------------------------

    def __init__(self):
        self.__reset_data()


    # -----------------------------
    # Helper methods
    # -----------------------------

    def __reset_data(self):
        """Reset all the data for a new simulation run."""

        self.mu = QueueSimulator.MU
        self.lamda = QueueSimulator.LAMDA


        self.waiting_queue = Queue()
        self.total_customers = 0
        self.total_time_spent_by_customers_in_system = []
        self.total_time_spent_by_customers_in_queue = []

        self.total_time_spent_in_queue = 0.0
        self.total_time_spent_in_system = 0.0

        self.total_busy_time = 0.0
        self.time_average_customers_in_system = 0.0
        self.time_average_customers_in_queue = 0.0
        self.customers_in_system_to_time_portion = {}
        self.customers_in_queue_to_time_portion = {}
        self.server_busy_flag = False


    def __get_next_event_data(self, next_arrival_time, next_departure_time):
        if next_arrival_time < next_departure_time:
            return QueueSimulator.QueueEvent.ARRIVAL, next_arrival_time
        else:
            return QueueSimulator.QueueEvent.DEPARTURE, next_departure_time

    # -----------------------------
    # Event methods
    # -----------------------------

    def __arrival_event(self, current_time , next_arrival_time, next_departure_time):
        """
        Adds a new customer to the system.
        If the server is busy, the customer is added to the waiting queue.
        else, the server starts serving the customer immediately.
        Returns the next arrival time and the next departure time.
        """

        next_arrival_time = current_time + expovariate(self.lamda)

        if not self.server_busy_flag:
            self.server_busy_flag = True
            next_departure_time = ((current_time, current_time + expovariate(self.mu)))
        else:
            self.waiting_queue.put(current_time)

        return next_arrival_time, next_departure_time

    def __departure_event(self, current_time, next_departure_time):
        """
        Adds a the departuring customer log to the system and updates the next departure time.
        Returns the next departure time.
        """
        self.total_time_spent_by_customers_in_system.append(next_departure_time)
        self.total_customers += 1

        if not self.waiting_queue.empty():
            self.server_busy_flag = True
            next_customer_arrival_time = self.waiting_queue.get()
            next_departure_time = ((next_customer_arrival_time, current_time + expovariate(self.mu)))
            self.total_time_spent_by_customers_in_queue.append((next_customer_arrival_time , current_time))
        else:
            self.server_busy_flag = False

        return next_departure_time

    def __update_customers_in_system_to_time_portion(self, prev_time, current_time):
        """
        Update customers in system to time portion
        The dictionary will map the number of customers in the system to a list of tuples cotaining
        the time intervals during which that number of customers was present in the system.
        eg. {0: [(0, 1)], 1: [(1, 2)]} means that there were 0 customers in the system from time 0 to 1, 1 customer from time 1 to 2.
        """

        # Get no. of customers in time span (prev_time, current_time)
        service_customer = 1 if self.server_busy_flag else 0
        customers_in_system = self.waiting_queue.qsize() + service_customer

        # Initialize the list for this number of customers if not already present
        if customers_in_system not in self.customers_in_system_to_time_portion:
            self.customers_in_system_to_time_portion[customers_in_system] = []

        self.customers_in_system_to_time_portion[customers_in_system].append((prev_time, current_time))

    def __update_customers_in_queue_to_time_portion(self, prev_time, current_time):
        """
        Update customers in queue to time portion
        The dictionary will map the number of customers in the queue to a list of tuples containing
        the time intervals during which that number of customers was present in the queue.
        """

        # Get no. of customers in queue in time span (prev_time, current_time)
        customers_in_queue = self.waiting_queue.qsize()

        # Initialize the list for this number of customers if not already present
        if customers_in_queue not in self.customers_in_queue_to_time_portion:
            self.customers_in_queue_to_time_portion[customers_in_queue] = []

        self.customers_in_queue_to_time_portion[customers_in_queue].append((prev_time, current_time))

    def __unload_queue_process(self, current_time, next_departure_time):
        """
        Processes the remaining customers in the queue after the simulation time ends (no arrivals afterwards).
        """

        prev_time = current_time
        current_time = next_departure_time[1]

        # Update the customers in system and queue to time portion
        self.__update_customers_in_system_to_time_portion(prev_time, current_time)
        self.__update_customers_in_queue_to_time_portion(prev_time, current_time)

        self.total_busy_time += (current_time - prev_time)

        next_departure_time = self.__departure_event(current_time, next_departure_time)

        return current_time, next_departure_time

    # -----------------------------
    # Main simulation method
    # -----------------------------
    def run_simulation(self, lamda=LAMDA, mu=MU, simulation_time=SIMULATION_TIME):

        self.__reset_data()

        if simulation_time <= 0:
            simulation_time = QueueSimulator.SIMULATION_TIME

        self.lamda = lamda if lamda > 0 else QueueSimulator.LAMDA
        self.mu = mu if mu > 0 else QueueSimulator.MU

        # Initialize the simulation parameters
        current_time = 0.0
        next_arrival_time = expovariate(self.lamda)
        next_departure_time = (0.0 , 0.0)       # (arrival_time, departure_time)

        while current_time < simulation_time:

            current_event , event_time = 0 , 0.0

            # Determine the next event
            if self.server_busy_flag:
                current_event, event_time = self.__get_next_event_data(next_arrival_time, next_departure_time[1])
            else:
                current_event = QueueSimulator.QueueEvent.ARRIVAL
                event_time = next_arrival_time

            # Update the current time
            prev_time = current_time
            current_time = event_time

            # Update customers in system to time portion
            self.__update_customers_in_system_to_time_portion(prev_time, current_time)

            # Update customers in queue to time portion
            self.__update_customers_in_queue_to_time_portion(prev_time, current_time)

            # Update busy time
            if self.server_busy_flag:
                self.total_busy_time += (current_time - prev_time)

            # HANDLE ARRIVAL
            if current_event == QueueSimulator.QueueEvent.ARRIVAL:
                next_arrival_time , next_departure_time = self.__arrival_event(current_time,
                                                                                       next_arrival_time,
                                                                                         next_departure_time)

            # HANDLE DEPARTURE
            else:
                next_departure_time = self.__departure_event(current_time, next_departure_time)


        # Handle remaining customers in the queue after simulation time
        while not self.waiting_queue.empty():
            current_time , next_departure_time = self.__unload_queue_process(current_time, next_departure_time)


        # Last departure event
        self.total_simulation_time , _ = self.__unload_queue_process(current_time, next_departure_time)

        # Calculate averages
        self.time_average_customers_in_system = self.__calculate_time_average_customers_in_system()
        self.time_average_customers_in_queue = self.__calculate_time_average_customers_in_queue()

        # Calculate total time spent in system and queue
        self.__calculate_total_time_spent_in_system()
        self.__calculate_total_time_spent_in_queue()

        # Calculate Queue metrics
        self.__calculate_queue_metrics()





    # -----------------------------
    # Calculation methods
    # -----------------------------
    def __calculate_time_average_customers_in_system(self):
        total_value = 0.0
        for customers_count in self.customers_in_system_to_time_portion:
            time_intervals = self.customers_in_system_to_time_portion[customers_count]
            for start, end in time_intervals:
                total_value += customers_count * (end - start)
        return total_value / self.total_simulation_time

    def __calculate_time_average_customers_in_queue(self):
        total_value = 0.0
        for customers_count in self.customers_in_queue_to_time_portion:
            time_intervals = self.customers_in_queue_to_time_portion[customers_count]
            for start, end in time_intervals:
                total_value += customers_count * (end - start)
        return total_value / self.total_simulation_time

    def __calculate_total_time_spent_in_system(self):
        for arrival_time, departure_time in self.total_time_spent_by_customers_in_system:
            self.total_time_spent_in_system += (departure_time - arrival_time)

    def __calculate_total_time_spent_in_queue(self):
        for arrival_time, departure_time in self.total_time_spent_by_customers_in_queue:
            self.total_time_spent_in_queue += (departure_time - arrival_time)

    def __calculate_customer_frequency_probability(self, n):
        intervals = self.customers_in_system_to_time_portion.get(n, [])
        total_duration = sum(end - start for start, end in intervals)
        return total_duration / self.total_simulation_time

    # -----------------------------
    # Queue metrics
    # -----------------------------

    def __calculate_queue_metrics(self):

        self.rho = self.total_busy_time / self.total_simulation_time

        self.Wq = self.total_time_spent_in_queue / self.total_customers

        self.Ws = self.total_time_spent_in_system / self.total_customers

        self.L = self.time_average_customers_in_system

        self.Lq = self.time_average_customers_in_queue

        self.P = []

        for n in range(4):
            self.P.append(self.__calculate_customer_frequency_probability(n))

    # -----------------------------
    # Print Queue metrics
    # -----------------------------

    def print_results(self):
        print(f"Utilization factor (ρ): {self.rho:.4f}")
        print(f"Average number of customers in the system (L): {self.L:.4f}")
        print(f"Average number of customers in the queue (Lq): {self.Lq:.4f}")
        print(f"Average time a customer spends in the system (Ws) in minutes: {self.Ws:.4f}")
        print(f"Average time a customer spends waiting in the queue (Wq) in minutes: {self.Wq:.4f}")
        print(f"P0-P3: {', '.join(f'{p:.4f}' for p in self.P)}")
