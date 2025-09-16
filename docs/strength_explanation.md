## Password Strength: What “bits” mean

### Entropy in bits
- **Definition**: Bits represent the amount of randomness (search space) in a password.
- **Formula used**: `entropy = log2(charset_size^length) = length * log2(charset_size)`
- **Charset size** comes from which character sets are present:
  - Lowercase: 26
  - Uppercase: 26
  - Digits: 10
  - Symbols (common): 32
  - If none detected, assume 95 printable ASCII

### How to interpret bits
- More bits = exponentially more possible passwords.
- Rough scale of total possibilities:
  - ~20 bits ≈ ~1 million
  - ~32 bits ≈ ~4.3 billion
  - ~40 bits ≈ ~1 trillion
  - ~48 bits ≈ ~281 trillion
  - ~64 bits ≈ ~1.8 × 10^19

### Cracking time intuition (very rough)
- Online (≈10^6 guesses/sec):
  - 32 bits: hours
  - 40 bits: days–weeks
  - 48 bits: years
  - 64 bits: far beyond practical timeframes
- Fast offline GPU (≈10^9 guesses/sec): subtract ~10 bits worth of time compared to above.

### Thresholds in this project
- Entropy color (visual cue):
  - ≥ 64 bits: Very strong (success)
  - ≥ 48 bits: Strong (info)
  - ≥ 32 bits: Moderate (warning)
  - <  32 bits: Weak (danger)

- Strength level (separate score-based label):
  - Computed from length, character variety, repetition penalties, and common-pattern checks.
  - Very Strong (score ≥ 80)
  - Strong (score ≥ 60)
  - Moderate (score ≥ 40)
  - Weak (score ≥ 20)
  - Very Weak (score < 20)

### Practical guidance
- Aim for **≥ 64 bits** of entropy and a **Strong/Very Strong** score.
- Use a long password with mixed character sets; avoid common patterns and repeats.

