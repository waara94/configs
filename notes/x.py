from collections import Counter, defaultdict
from itertools import zip_longest
import numpy as np
from scipy.stats import entropy


def analyze_ngrams(ciphertext, n=2):
    ciphertext = ciphertext.replace(" ", "")
    ngrams = [ciphertext[i : i + n] for i in range(len(ciphertext) - n + 1)]
    ngram_counts = Counter(ngrams)
    total_ngrams = len(ngrams)
    print(f"Top 10 most frequent {n}-grams:")
    for ngram, count in ngram_counts.most_common(10):
        freq = count / total_ngrams * 100
        print(f"{ngram}: {count} occurrences ({freq:.2f}%)")


def check_length_factors(ciphertext):
    length = len(ciphertext.replace(" ", ""))
    print(f"Ciphertext length: {length}")
    factors = [i for i in range(1, length + 1) if length % i == 0]
    print("Possible block/key sizes (factors):")
    for factor in factors:
        if factor > 1:
            print(f"{factor} (divides evenly into {length})")


def calculate_entropy_scipy(ciphertext):
    """Calculate Shannon entropy using SciPy's entropy function."""
    ciphertext = ciphertext.replace(" ", "")
    length = len(ciphertext)
    char_counts = Counter(ciphertext)
    probabilities = [count / length for count in char_counts.values()]
    ent = entropy(probabilities, base=2)
    max_entropy = 4.70044  # log2(26)

    print(f"Entropy: {ent:.2f} bits per character")
    print(f"Maximum entropy (26 letters): {max_entropy:.2f} bits")
    print(f"Randomness ratio: {ent / max_entropy:.2f}")


def markov_transitions(ciphertext, alphabet_size=26):
    """Build and analyze a Markov transition matrix for adjacent characters."""
    ciphertext = ciphertext.replace(" ", "").upper()

    # Map characters to indices (assuming A-Z for simplicity)
    char_to_idx = {chr(65 + i): i for i in range(alphabet_size)}
    idx_to_char = {i: chr(65 + i) for i in range(alphabet_size)}

    # Initialize transition matrix
    transition_matrix = np.zeros((alphabet_size, alphabet_size))
    transitions = defaultdict(int)
    total_transitions = 0

    # Count transitions
    for i in range(len(ciphertext) - 1):
        if ciphertext[i] in char_to_idx and ciphertext[i + 1] in char_to_idx:
            row = char_to_idx[ciphertext[i]]
            col = char_to_idx[ciphertext[i + 1]]
            transition_matrix[row, col] += 1
            transitions[(ciphertext[i], ciphertext[i + 1])] += 1
            total_transitions += 1

    # Normalize to probabilities
    if total_transitions > 0:
        transition_matrix /= total_transitions

    # Display top transitions
    print("Top 10 most frequent transitions:")
    sorted_transitions = sorted(transitions.items(), key=lambda x: x[1], reverse=True)
    for (char1, char2), count in sorted_transitions[:10]:
        prob = count / total_transitions * 100
        print(f"{char1} -> {char2}: {count} occurrences ({prob:.2f}%)")

    # Analyze matrix uniformity
    flat_probs = transition_matrix.flatten()
    uniform_entropy = entropy(flat_probs, base=2)
    max_entropy = np.log2(alphabet_size * alphabet_size)  # Max for 26x26 matrix
    print(f"\nTransition matrix entropy: {uniform_entropy:.2f} bits")
    print(f"Maximum entropy (uniform 26x26): {max_entropy:.2f} bits")
    print(f"Uniformity ratio: {uniform_entropy / max_entropy:.2f}")

    return transition_matrix


def transpose_strings(strings):
    if not strings:
        return []
    max_length = max(len(s) for s in strings)  # Find the longest string length
    transposed = []
    for i in range(max_length):
        transposed.append(''.join(s[i] for s in strings if i < len(s)))
    return transposed


def transpose_strings(strings):
    return [''.join(filter(None, chars)) for chars in zip_longest(*strings, fillvalue=None)]





p_values = np.array([0.01, 0.04, 0.02, 0.001, 0.05, 0.20, 0.15, 0.003])
reject, pvals_corrected, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
significant_pvals = p_values[reject]
print("P-values that should be rejected:", significant_pvals)





p_values = np.array([0.01, 0.04, 0.02, 0.001, 0.05, 0.20, 0.15, 0.003])
methods = ['bonferroni', 'holm', 'fdr_bh', 'fdr_by']
results = {}
for method in methods:
    reject, pvals_corrected, _, _ = multipletests(p_values, alpha=0.05, method=method)
    results[method] = (reject, pvals_corrected)
for method, (reject, pvals_corrected) in results.items():
    print(f"\nMethod: {method}")
    print("Adjusted p-values:", pvals_corrected)
    print("Reject Null Hypothesis:", reject)




def longest_common_substrings(strings: list[str], n: int):
    """
    Finds the top n longest common substrings among all given strings.

    :param strings: A list or set of strings.
    :param n: Number of longest common substrings to return.
    :return: A list of top n longest common substrings sorted by length.
    """
    if not strings or len(strings) < 2:
        return []

    shortest_str = min(strings, key=len)
    substrings = set()

    for i in range(len(shortest_str)):
        for j in range(i + 1, len(shortest_str) + 1):
            substr = shortest_str[i:j]
            if all(substr in s for s in strings):
                substrings.add(substr)

    sorted_substrings = sorted(substrings, key=len, reverse=True)

    return sorted_substrings[:n]


strings = ["broadcaster", "broadcasting", "broadcast"]
n = 3
print(longest_common_substrings(strings, n))
