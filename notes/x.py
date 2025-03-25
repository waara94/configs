from collections import Counter, defaultdict

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
