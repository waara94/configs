from collections import Counter

from scipy.stats import chisquare


def chi_square_randomness_test(
    sequence: str, alpha: float, alphabet_size: int
) -> tuple[bool, float, float]:
    """
    Performs a chi-square goodness-of-fit test to determine if a sequence appears random.

    Args:
        sequence (str): The input string sequence to test.
        alpha (float): Significance level (typically 0.05 or 0.01).
        alphabet_size (int): Number of possible symbols in the alphabet.

    Returns:
        tuple[bool, float, float]: (is_random, chi_square_stat, p_value) where:
            - is_random: True if sequence appears random (fails to reject H0).
            - chi_square_stat: The calculated chi-square statistic.
            - p_value: The p-value from the test.

    Raises:
        ValueError: If inputs are invalid.
    """

    # Input validation
    if not isinstance(sequence, str) or not sequence:
        raise ValueError("Sequence must be a non-empty string")
    if not isinstance(alpha, float) or not 0 < alpha < 1:
        raise ValueError("Alpha must be a float between 0 and 1")
    if not isinstance(alphabet_size, int) or alphabet_size <= 0:
        raise ValueError("Alphabet size must be a positive integer")

    # Compute observed frequencies
    observed_counts = Counter(sequence)
    observed_counts = [x for x in list(observed_counts.values())] + [0] * (
        alphabet_size - len(set(sequence))
    )
    print(observed_counts)

    # Expected frequencies assuming a uniform distribution
    n = len(sequence)
    expected_frequencies = [n / alphabet_size] * alphabet_size
    print(expected_frequencies)

    chi_stat, p_value = chisquare(
        f_obs=observed_counts,
        f_exp=expected_frequencies,
        ddof=0,
    )

    # Decision: if p-value < alpha, reject H0 (sequence is not random)
    is_random = p_value >= alpha

    return is_random, chi_stat, p_value


if __name__ == "__main__":
    # Example matching your rat experiment (3 categories, 90 trials)
    sequence = "101010101010"  # Simulated input
    result, chi_stat, p = chi_square_randomness_test(
        sequence, alpha=0.05, alphabet_size=2
    )

    print(f"Chi-square statistic: {chi_stat:.2f}")
    print(f"P-value: {p}")
    print(f"Conclusion: {'Random' if result else 'Not random'}")
