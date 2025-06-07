from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWidget(FigureCanvas):
    def __init__(self, data, sim_data=None, parent=None):
        fig = Figure(figsize=(6, 4))
        super().__init__(fig)
        self.setParent(parent)

        self.ax = fig.add_subplot(111)
        self.plot(data, sim_data)

    def plot(self, data, sim_data=None):
        rho_values = data["rho_values"]
        Wq_values = data["Wq_values"]

        self.ax.clear()
        # Plot theoretical curve
        self.ax.plot(rho_values, Wq_values, label='Theoretical $W_q$ (minutes)', linewidth=2)

        # Plot simulation points if provided
        if sim_data is not None:
            rho_sim = sim_data.get("rho_sim")
            Wq_sim = sim_data.get("Wq_sim")
            if rho_sim is not None and Wq_sim is not None:
                self.ax.scatter(rho_sim, Wq_sim, color='red', label='Simulation $W_q$', zorder=5)

        self.ax.set_xlabel('Utilization factor (ρ)')
        self.ax.set_ylabel('Average waiting time in queue $W_q$ (minutes)')
        self.ax.set_title('Average Waiting Time in Queue vs Utilization Factor')
        self.ax.grid(True)
        self.ax.legend()
        self.draw()
