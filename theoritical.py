def calculate_queue_metrics(lamda, mu):
    """
    Calculate queue metrics for an M/M/1 queue.
    
    Parameters:
    lamda (float): Arrival rate (customers per time unit)
    mu (float): Service rate (customers served per time unit)
    
    Returns:
    str: Formatted string with calculated metrics
    """
    if lamda <= 0 or mu <= 0:
        return "Arrival rate and service rate must be greater than zero."

    # Utilization factor
    rho = lamda / mu

    # Average number of customers in the system (L)
    L = rho / (1 - rho)

    # Average number of customers in the queue (Lq)
    Lq = rho**2 / (1 - rho)

    # Average time a customer spends in the system (W)
    Ws = 1 / (mu - lamda)


    # Average time a customer spends waiting in the queue (Wq)
    Wq = lamda / (mu * (mu - lamda))

    # Probability of n customers in the system (P0, P1, P2, P3)
    P = [(1 - rho) * (rho ** n) for n in range(4)]

    results = (
        f"Utilization factor (ρ): {rho:.4f}\n"
        f"Average number of customers in the system (L): {L:.4f}\n"
        f"Average number of customers in the queue (Lq): {Lq:.4f}\n"
        f"Average time a customer spends in the system (Ws) in hours: {Ws:.4f} in minutes: {Ws * 60:.4f}\n"
        f"Average time a customer spends waiting in the queue (Wq) in hours: {Wq:.4f} in minutes: {Wq * 60:.4f}\n"
        f"P0-P3: {', '.join(f'{p:.4f}' for p in P)}"
    )

    data = [
        rho,
        Wq * 60
    ]
    return results, data