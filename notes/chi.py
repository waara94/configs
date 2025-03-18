import numpy as np
from scipy.stats import chisquare


def chi2_randomness_test(sample, n_symbols: int, alpha=0.05):
    """
    Performs a Chi-Square Goodness of Fit test to check if a sample appears randomly distributed
    across its unique symbols.

    Parameters:
        sample (list): A list of categorical symbols (e.g., ['A', 'B', 'C', ...])
        alpha (float): Significance level for the test (default: 0.05)

    Returns:
        dict: A dictionary with chi-square statistic, p-value, and interpretation
    """
    if not sample:
        raise ValueError("Empty sample")

    symbols, counts = np.unique(
        sample, return_counts=True
    )  # Get unique symbols and their counts
    print(symbols)
    print(counts)

    expected_counts = np.full(
        n_symbols, len(sample) / n_symbols
    )  # Uniform expected distribution

    chi2_stat, p_value = chisquare(counts, expected_counts)  # Chi-square test

    if p_value >= alpha:
        hypothesis = "H0: not rejected (sample appears random)"
    else:
        hypothesis = "H0: rejected (sample does not appear random)"

    result = {"chi2_stat": chi2_stat, "p_value": p_value, "hypothesis": hypothesis}

    return result


# Example usage
sample_data = [
    "A",
    "B",
    "C",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "A",
    "B",
    "C",
]
alpha_value = 0.05  # Customizable p-value threshold
result = chi2_randomness_test(sample_data, n_symbols=9, alpha=alpha_value)

# Print results
print(f"Chi-Square Statistic: {result['chi2_stat']}")
print(f"P-value: {result['p_value']}")
print(f"Interpretation: {result['hypothesis']}")
