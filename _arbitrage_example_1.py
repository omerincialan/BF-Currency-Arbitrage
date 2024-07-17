# This is the simple arbitrage case in the presentation
# USD - EUR - GBP

import math

def bellman_ford(graph, start):
    # Step 1: Initialize distances from start to all other vertices as infinity
    distances = {v: float('inf') for v in graph}
    predecessors = {v: None for v in graph}
    distances[start] = 0

    # Step 2: Relax all edges |V| - 1 times
    for _ in range(len(graph) - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u

    # Step 3: Check for negative-weight cycles
    for u in graph:
        for v, weight in graph[u].items():
            if distances[u] + weight < distances[v]:
                # Negative cycle found
                cycle = []
                current = v
                while current not in cycle:
                    cycle.append(current)
                    current = predecessors[current]
                cycle.append(current)
                cycle = cycle[::-1]
                return cycle

    return None

def find_arbitrage_opportunities(exchange_rates):
    # Build the graph
    graph = {}
    currencies = list(exchange_rates.keys())
    for currency in currencies:
        graph[currency] = {}
        for target_currency in currencies:
            if currency != target_currency:
                rate = exchange_rates[currency][target_currency]
                graph[currency][target_currency] = -math.log(rate)

    # Run Bellman-Ford algorithm to detect negative cycles
    for currency in currencies:
        cycle = bellman_ford(graph, currency)
        if cycle:
            return cycle

    return None

# Sample exchange rates
exchange_rates = {
    'USD': {'EUR': 0.9, 'GBP': 0.75, 'JPY': 110.0},
    'EUR': {'USD': 1.1, 'GBP': 0.83, 'JPY': 122.0},
    'GBP': {'USD': 1.33, 'EUR': 1.2, 'JPY': 146.0},
    'JPY': {'USD': 0.009, 'EUR': 0.0082, 'GBP': 0.0068}
}
# This is the sample case used in the presentation.
exchange_rates2 = {
    'USD': {'EUR': 0.9, 'GBP': 1, 'JPY': 1},
    'EUR': {'USD': 1, 'GBP': 1.2, 'JPY': 1},
    'GBP': {'USD': 1.1, 'EUR': 1, 'JPY': 1},
    'JPY': {'USD': 1, 'EUR': 1, 'GBP': 1}
}

exchange_rates3 = {
    'USD': {'EUR': 1, 'GBP': 1, 'JPY': 1},
    'EUR': {'USD': 1, 'GBP': 1, 'JPY': 1},
    'GBP': {'USD': 1, 'EUR': 1, 'JPY': 1},
    'JPY': {'USD': 1, 'EUR': 1, 'GBP': 1}
}

cycle = find_arbitrage_opportunities(exchange_rates2)
if cycle:
    print("Arbitrage opportunity detected:")
    for i in range(len(cycle) - 1):
        print(f"{cycle[i]} -> {cycle[i+1]}")
    print(f"{cycle[-1]} -> {cycle[0]}")
else:
    print("No arbitrage opportunity detected.")
