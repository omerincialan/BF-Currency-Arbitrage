# This is the real life implementation of
# currency arbitrage detection by using Bellman-Ford's Algorithm.
# I added visualization part.
#SOURCE: https://gist.github.com/anilpai/08f3cedb60b7a3c9a3b4e27c0c022096

import requests
from typing import Tuple, List
from math import log
import networkx as nx
import matplotlib.pyplot as plt

currencies = ( 'EUR', 'USD', 'MXN', 'CAD', 'AUD','CHF', 'TRY')
api_key = 'fe69bd3037f74f699cf2bf8070b44374'

def get_rates(currencies: Tuple[str, ...], api_key: str) -> List[List[float]]:
    rates = []
    response = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={api_key}')
    data = response.json()['rates']
    rates_to_usd = {currency: data.get(currency, 0) for currency in currencies}

    for currency in currencies:
        rates.append([rates_to_usd[currency] / rates_to_usd[curr] if rates_to_usd[curr] != 0 else 0 for curr in currencies])
    return rates

def negate_logarithm_convertor(graph: Tuple[Tuple[float]]) -> List[List[float]]:
    ''' log of each rate in graph and negate it'''
    result = [[-log(edge) if edge != 0 else float('inf') for edge in row] for row in graph]
    return result

def arbitrage(currency_tuple: tuple, rates_matrix: Tuple[Tuple[float, ...]]) -> List[List[int]]:
    ''' Calculates arbitrage situations and prints out the details of this calculations'''

    trans_graph = negate_logarithm_convertor(rates_matrix)

    n = len(trans_graph)
    min_dist = [float('inf')] * n
    pre = [-1] * n
    arbitrage_paths = []

    for source in range(n):
        min_dist[source] = 0

        for _ in range(n-1):
            for source_curr in range(n):
                for dest_curr in range(n):
                    if source_curr == dest_curr or trans_graph[source_curr][dest_curr] == float('inf'):
                        continue
                    if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                        min_dist[dest_curr] = min_dist[source_curr] + trans_graph[source_curr][dest_curr]
                        pre[dest_curr] = source_curr

        for source_curr in range(n):
            for dest_curr in range(n):
                if source_curr == dest_curr or trans_graph[source_curr][dest_curr] == float('inf'):
                    continue
                if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                    print_cycle = [dest_curr, source_curr]
                    while pre[source_curr] not in print_cycle:
                        source_curr = pre[source_curr]
                        print_cycle.append(source_curr)
                    print_cycle.append(pre[source_curr])
                    if print_cycle[0] == print_cycle[-1]:
                        cycle_path = print_cycle[::-1]
                        arbitrage_paths.append(cycle_path)
                        print(f"Arbitrage Opportunity: \n{' --> '.join([currency_tuple[p] for p in cycle_path])}")

    return arbitrage_paths


def visualize_graph(currencies: Tuple[str, ...], rates: List[List[float]], arbitrage_paths: List[List[int]]):
    G = nx.DiGraph()
    n = len(currencies)

    for i in range(n):
        for j in range(n):
            if rates[i][j] != 0 and rates[i][j] != float('inf'):
                G.add_edge(currencies[i], currencies[j], weight=rates[i][j])

    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=15, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    for path in arbitrage_paths:
        edges = [(currencies[path[i]], currencies[path[i + 1]]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='green', width=2)

    plt.title("Currency Exchange Graph and Arbitrage Opportunities")
    plt.show()

if __name__ == "__main__":
    rates = get_rates(currencies, api_key)
    arbitrage_paths = arbitrage(currencies, rates)
    visualize_graph(currencies, rates, arbitrage_paths)
