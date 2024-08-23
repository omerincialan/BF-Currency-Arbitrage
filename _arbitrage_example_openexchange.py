# This is the real life implementation of
# currency arbitrage detection by using Bellman-Ford's Algorithm.
# I added visualization part.
#SOURCE: https://gist.github.com/anilpai/08f3cedb60b7a3c9a3b4e27c0c022096

import requests
from typing import Tuple, List
from math import log
import networkx as nx
import matplotlib.pyplot as plt

currencies = ('CAD', 'EUR', 'USD', 'RUB', 'CHF', 'TRY', 'MXN') # defining a tuple here
api_key = 'bfdab30d40bd42c3b12a4e5e9e40898a'

def get_rates(currencies: Tuple[str, ...], api_key: str) -> List[List[float]]:
    rates = [] # initializing an empty list
    response = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={api_key}') #sending a get request
    data = response.json()['rates'] # we are extracting the json response  here in this list
    rates_to_usd = {currency: data.get(currency, 0) for currency in currencies} # creationg another dictionarty where we keep each currency's rate against US dollar

    for currency in currencies:
        rates.append([rates_to_usd[currency] / rates_to_usd[curr] if rates_to_usd[curr] != 0 else 0 for curr in currencies])
    return rates

def negate_logarithm_convertor(graph: Tuple[Tuple[float]]) -> List[List[float]]:
    ''' log of each rate in graph and negate it'''

    result = [[-log(edge) if edge != 0 else float('inf') for edge in row] for row in graph]
    return result

# This function takes tuple of currencies, matrix of exchange rates and arbitrage paths we derive from another function
# we use built in graph library of python here.
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

# this is the main loop, where we apply bellman-ford algorithm on the graph.
# I have another video where I explain the working logic of BF. If you are into algorithms you can have a look at it.
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

if __name__ == "__main__":
    rates = get_rates(currencies, api_key)
    arbitrage_paths = arbitrage(currencies, rates)
    visualize_graph(currencies, rates, arbitrage_paths)
    # here we are calling all the functions.
    # we could improve the code so that it prints the arbotrage amount. I mean, If we buy 10K with how much money we end up.
