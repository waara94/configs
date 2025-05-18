import itertools
from collections import Counter

import statsmodels.stats.diagnostic as smd
from scipy.stats import chi2_contingency, chisquare, entropy
from tabulate import tabulate

# Assuming ALPHABET is a global variable, e.g., ALPHABET = 'abc' for symbols 'a', 'b', 'c'

ALPHABET = "abcd"


def symbol_frequency_test(data, alphabet=ALPHABET):
    """
    Performs a chi-square test on symbol frequencies to assess uniformity.

    Parameters:
    - data: str, input data as a string
    - alphabet: str, the alphabet of symbols (default: global ALPHABET)

    Returns:
    - tuple: (chi2 statistic, p-value)
    """
    counter = Counter(data)
    observed = [counter.get(symbol, 0) for symbol in alphabet]
    chi2, p = chisquare(observed)
    return chi2, p


def bigram_frequency_test(data, alphabet=ALPHABET):
    """
    Performs a chi-square test on bigram frequencies to assess uniformity.

    Parameters:
    - data: str, input data as a string
    - alphabet: str, the alphabet of symbols (default: global ALPHABET)

    Returns:
    - tuple: (chi2 statistic, p-value)
    """
    n = len(alphabet)
    all_bigrams = list(itertools.product(alphabet, repeat=2))
    bigrams = zip(data, data[1:])
    counter = Counter(bigrams)
    observed = [counter.get(pair, 0) for pair in all_bigrams]  # type: ignore
    chi2, p = chisquare(observed)
    return chi2, p


def markov_transition_test(data, alphabet=ALPHABET, print_matrix=False):
    """
    Performs chi-square tests on each row of the Markov transition matrix and optionally prints the transition probability matrix.

    Parameters:
    - data: str, input data as a string
    - alphabet: str, the alphabet of symbols (default: global ALPHABET)
    - print_matrix: bool, whether to print the transition matrix (default: False)

    Returns:
    - dict: symbol -> (chi2 statistic, p-value) for each symbol's transitions, or (None, None) if no transitions
    """
    n = len(alphabet)
    # Build transition counts as a dictionary of Counters
    transition_counts = {s1: Counter() for s1 in alphabet}
    for s1, s2 in zip(data, data[1:]):
        transition_counts[s1][s2] += 1

    # Compute transition probabilities
    transition_matrix = {}
    for s1 in alphabet:
        total = sum(transition_counts[s1].values())
        if total > 0:
            transition_matrix[s1] = {
                s2: transition_counts[s1][s2] / total for s2 in alphabet
            }
        else:
            transition_matrix[s1] = {s2: 0.0 for s2 in alphabet}

    # Print the transition matrix using tabulate if requested
    if print_matrix:
        # Prepare table data: each row is [symbol, prob_s1, prob_s2, ...]
        table = []
        for s1 in alphabet:
            row = [s1] + [f"{transition_matrix[s1][s2]:.2f}" for s2 in alphabet]
            table.append(row)
        # Column headers: empty first column (for row labels), then alphabet
        headers = [""] + list(alphabet)
        print(tabulate(table, headers=headers, tablefmt="simple", floatfmt=".2f"))

    # Perform chi-square test for each symbol's transitions
    results = {}
    for s1 in alphabet:
        observed = [transition_counts[s1].get(s2, 0) for s2 in alphabet]
        total = sum(observed)
        if total > 0:  # Only test if there are transitions
            chi2, p_value = chisquare(observed)
            results[s1] = p_value
        else:
            results[s1] = (None, None)  # No transitions
    return results


def autocorrelation_test(data, alphabet=ALPHABET, nlags=10):
    """
    Performs the Ljung-Box test for autocorrelation up to specified lags.

    Parameters:
    - data: str, input data as a string
    - alphabet: str, the alphabet of symbols (default: global ALPHABET)
    - nlags: int, number of lags to test (default: 10)

    Returns:
    - tuple: (test statistics array, p-values array) for each lag
    """
    if len(data) <= nlags:
        raise ValueError("Data length must exceed number of lags")
    symbol_to_index = {s: i for i, s in enumerate(alphabet)}
    numerical_data = [symbol_to_index[s] for s in data]
    result = smd.acorr_ljungbox(numerical_data, lags=nlags)
    return result


def entropy_test(data, alphabet=ALPHABET):
    """
    Computes the Shannon entropy of the symbol distribution.

    Parameters:
    - data: str, input data as a string
    - alphabet: str, the alphabet of symbols (default: global ALPHABET)

    Returns:
    - float: Shannon entropy in bits
    """
    counter = Counter(data)
    return entropy(list(counter.values()), base=2)


def lagged_pair_chi2(data, alphabet=ALPHABET, lag=1):
    """
    Build an n×n contingency table of (symbol_t, symbol_{t+lag}) pairs
    and run a chi-square test of independence.

    Parameters
    ----------
    data : str
        The sequence of symbols.
    alphabet : iterable
        The list or string of all possible symbols, length n.
    lag : int
        The offset between positions to test.

    Returns
    -------
    chi2 : float
        The Pearson chi-square statistic.
    p : float
        The p-value for the test (df = (n-1)^2).
    table : list of lists
        The observed counts table (rows=current symbol, cols=next symbol).
    """
    n = len(alphabet)
    idx = {s: i for i, s in enumerate(alphabet)}

    # Count all valid (t, t+lag) pairs
    pairs = []
    for t in range(len(data) - lag):
        a, b = data[t], data[t + lag]
        if a in idx and b in idx:
            pairs.append((a, b))

    # Build observed table
    counts = Counter(pairs)
    table = [[counts[(a, b)] for b in alphabet] for a in alphabet]

    # chi2_contingency assumes the table is frequency counts
    chi2, p, dof, expected = chi2_contingency(table, correction=False)
    return chi2, p, table


# Example usage:
data = "abacbbcacbabcbcbacaaaabcccaabcd" * 10
data = "".join("a" if (i + 1) % 3 == 0 else char for i, char in enumerate(data))
chi2, pval, obs_table = lagged_pair_chi2(data, alphabet="abc", lag=3)

print(f"Lag-1 pair χ² = {chi2:.2f}, p = {pval}")
print("Observed contingency table (rows=curr, cols=next):")
for row in obs_table:
    print("  ", row)


# # Example usage (uncomment to test):
# data = "abacbbcacbabcbcbacaaaabcccaabcd" * 10
# # print("Symbol Frequency:", symbol_frequency_test(data))
# # print("Bigram Frequency:", bigram_frequency_test(data))
# print("Markov Transitions:", markov_transition_test(data, print_matrix=True))
# # print("Autocorrelation:\n", autocorrelation_test(data))
# # print("Entropy:", entropy_test(data), "vs max", math.log2(len(ALPHABET)))
