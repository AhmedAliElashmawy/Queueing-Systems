import matplotlib.pyplot as plt

def PlotWidget(results):
    # Extract data from results
    rho = results[0]
    wq = results[1]
    # Create a plot using the extracted data

    plt.figure(figsize=(10, 6))
    plt.plot(rho,wq, label="Theoretical Wq", marker='o', color='blue')
    plt.title("Queueing System Metrics")
    plt.xlabel("Utilization Factor (ρ)")
    plt.ylabel("Average Waiting Time in Queue (Wq) in minutes")
    plt.grid(True)
    plt.legend()
    return plt.gcf()
