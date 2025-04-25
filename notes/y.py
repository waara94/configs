cnt = Counter(d for tpl in data for d in tpl)

def adjacency_counts(data):
    """
    Count how often x at pos i is followed by y at pos i+1.
    Returns a dict:  { (i, x, y): count } for i in 0..5
    """
    adj = Counter()
    for tpl in data:
        for i in range(6):
            adj[(i, tpl[i], tpl[i+1])] += 1
    # convert to nested structure if you like
    return dict(adj)


def positional_freq(data):
    """For each position, count occurrences of each digit."""
    pos_freq = [Counter() for _ in range(7)]
    for tpl in data:
        for i, d in enumerate(tpl):
            pos_freq[i][d] += 1
    return [dict(c) for c in pos_freq]


def build_transition_matrix(data, n=1):
    # count n-gram → next‐digit
    trans = defaultdict(Counter)
    for tpl in data:
        for i in range(len(tpl) - n):
            key = tuple(tpl[i:i+n])
            trans[key][tpl[i+n]] += 1
    # normalize into probabilities
    probs = {
        key: {d: cnt/sum(cnts.values()) for d, cnt in cnts.items()}
        for key, cnts in trans.items()
    }
    return probs

# usage
bigram_probs = build_transition_matrix(data, n=2)


def entropy(tpl):
    cnt = Counter(tpl)
    total = len(tpl)
    return -sum((c/total)*math.log2(c/total) for c in cnt.values())



def markov_transition_matrix(data):
    """
    data: list of 7-tuples with digits 0–9
    Returns: 10x10 dict of normalized transition probabilities
    """
    transitions = defaultdict(Counter)

    for tpl in data:
        for i in range(len(tpl) - 1):
            a, b = tpl[i], tpl[i+1]
            transitions[a][b] += 1

    # Normalize each row to make probabilities
    matrix = {}
    for a in range(10):
        total = sum(transitions[a].values())
        if total == 0:
            matrix[a] = {b: 0.0 for b in range(10)}
        else:
            matrix[a] = {b: transitions[a][b] / total for b in range(10)}

    return matrix


import networkx as nx

def build_transition_graph(data):
    """
    Constructs a directed graph from list of 7-tuples of digits (0-9).
    Edges have weights equal to observed transition frequencies.
    """
    G = nx.DiGraph()
    transition_counts = Counter()

    # Count transitions
    for tpl in data:
        for i in range(len(tpl) - 1):
            a, b = tpl[i], tpl[i + 1]
            transition_counts[(a, b)] += 1

    # Add weighted edges to the graph
    for (a, b), weight in transition_counts.items():
        G.add_edge(a, b, weight=weight)

    return G


def draw_weighted_graph(G, min_weight=1):
    """
    Draws the transition graph, showing edges with weight ≥ min_weight.
    """
    pos = nx.spring_layout(G, seed=42)  # layout algorithm
    edge_weights = nx.get_edge_attributes(G, "weight")

    # Filter edges
    filtered_edges = {k: v for k, v in edge_weights.items() if v >= min_weight}

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=12)

    # Draw only filtered edges
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=filtered_edges.keys(),
        width=[v / 2 for v in filtered_edges.values()],
        arrowstyle="->",
        arrowsize=10,
    )
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels={k: str(v) for k, v in filtered_edges.items()}, font_size=10
    )
    plt.title("Digit Transition Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


data = [
    (1, 2, 3, 4, 5, 6, 7),
    (2, 3, 5, 2, 6, 7, 8),
    (3, 4, 5, 6, 7, 8, 9),
    (4, 5, 6, 7, 8, 9, 0),
    # ... more samples
]

G = build_transition_graph(data)
draw_weighted_graph(G, min_weight=1)
