import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src/logic')))


from simulation import QueueSimulator
from theoritical import calculate_queue_metrics


# Convert from hourly rate to minutely rate
TO_MINUTES_RATE = lambda x: x * 60




def present_theoretical_results(lamda , mu):
    results, data = calculate_queue_metrics(lamda, mu)
    print("Theoretical Results:")
    print(results)
    print("-" * 50)


def present_simulation_results(lamda, mu):
    simulator = QueueSimulator()
    simulator.run_simulation(lamda, mu)

    print("Simulation Results:")
    simulator.print_results()




def run_test(scenario):
    lamda = (scenario["lamda"])
    mu = (scenario["mu"])

    present_theoretical_results(lamda, mu)

    present_simulation_results(lamda, mu)


if __name__ == "__main__":

    # Tests
    scenarios =[
        {"mu": 12, "lamda": 4},
        {"mu": 12, "lamda": 6},
        {"mu": 12, "lamda": 10}
    ]



    for scenario in scenarios:
        print(f"Running test with λ = {scenario['lamda']} hours, μ = {scenario['mu']} hours")
        run_test(scenario)
        print("\n" + "="*50 + "\n")




