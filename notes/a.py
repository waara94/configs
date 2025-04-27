import math
from collections import Counter
from itertools import product

import numpy as np
from scipy.stats import chisquare
from statsmodels import stats


def entropy_test(data: str, alphabet: list[str]):
    n = len(data)
    observed_probs = np.array([data.count(symbol) / n for symbol in alphabet])
    entropy = -np.sum([p * math.log2(p) for p in observed_probs if p > 0])
    max_entropy = math.log2(len(alphabet))
    return entropy, entropy / max_entropy


def serial_test(data: str, alphabet: list[str], tuple_size=2):
    if len(data) < tuple_size:
        raise ValueError("Sample too small")

    # Form all overlapping n-grams from the data
    ngrams = [
        tuple(data[i : i + tuple_size]) for i in range(len(data) - tuple_size + 1)
    ]

    # Count observed n-grams
    observed_counts = Counter(ngrams)

    # Generate all possible n-grams
    all_possible_ngrams = list(product(alphabet, repeat=tuple_size))

    # Build observed and expected counts
    observed = np.array([observed_counts.get(gram, 0) for gram in all_possible_ngrams])
    print(observed_counts)
    print(observed)
    expected = np.full(len(all_possible_ngrams), len(ngrams) / len(all_possible_ngrams))

    # Chi-Square Test
    chi2, p_value = chisquare(f_obs=observed, f_exp=expected)

    return chi2, p_value


def runs_test(data, alphabet=None):
    if len(data) < 2:
        return 0.0, 1.0

    # Count the number of runs
    runs = 1
    for i in range(1, len(data)):
        if data[i] != data[i - 1]:
            runs += 1

    n = len(data)
    if alphabet is not None:
        k = len(alphabet)  # True alphabet size provided
    else:
        k = len(set(data))  # Fallback: infer from data

    if k < 2:
        return 0.0, 1.0  # not meaningful if only one symbol

    # Expected number of runs
    expected_runs = (2 * n - k) / (k + 1)

    # Standard deviation
    std_dev_runs = math.sqrt((2 * n * (2 * n - k - 1)) / ((k + 1) ** 2 * (k + 2)))

    # Z-score and p-value
    z = (runs - expected_runs) / std_dev_runs
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return z, p_value


from scipy import stats


def runs_test_alphabet_size(data, k):
    """
    Multi-symbol runs test parameterized by alphabet size.

    Args:
        data (list or str): sequence of symbols.
        k (int): total number of distinct symbols in the alphabet.

    Returns:
        runs (int): observed number of runs.
        expected_runs (float): E[R] = 1 + (n² – Σ n_j²) / n.
        std_dev (float): approximate σ = sqrt((n–1)·p·(1–p)).
        z_score (float): (runs – expected_runs) / std_dev.
        p_value (float): two-tailed normal p-value.

    Raises:
        ValueError: if k < number of distinct symbols actually seen in data.
    """
    n = len(data)
    if n < 2:
        return 0, 0.0, 1.0, 0.0, 1.0

    # 1) Count runs
    runs = 1
    for i in range(1, n):
        if data[i] != data[i - 1]:
            runs += 1

    # 2) Count observed symbol frequencies
    counts = list(Counter(data).values())
    distinct_obs = len(counts)
    if distinct_obs > k:
        raise ValueError(
            f"Data has {distinct_obs} distinct symbols, but k = {k} < {distinct_obs}"
        )

    # 3) Compute sum of squares of counts (zeros for missing symbols contribute 0)
    sum_nj_sq = sum(c * c for c in counts)

    # 4) Expected runs: 1 + (n² – Σ n_j²) / n
    expected_runs = 1.0 + (n * n - sum_nj_sq) / n

    # 5) Probability of a change between adjacent symbols:
    #    p = (n² – Σ n_j²) / (n·(n–1))
    p_change = (n * n - sum_nj_sq) / (n * (n - 1))

    #    Variance ≈ (n–1)·p·(1–p)
    var_runs = (n - 1) * p_change * (1 - p_change)
    std_dev = math.sqrt(var_runs) if var_runs > 0 else 0.0

    # 6) Z-score and two-tailed p-value
    z_score = (runs - expected_runs) / std_dev if std_dev > 0 else 0.0
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    return runs, expected_runs, std_dev, z_score, p_value

