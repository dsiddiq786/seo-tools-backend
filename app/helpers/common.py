def count_syllables(word: str) -> int:
    """Count the number of syllables in a word."""
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    previous_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not previous_char_was_vowel:
                count += 1
            previous_char_was_vowel = True
        else:
            previous_char_was_vowel = False
    if word.endswith("e"):
        count -= 1
    return max(1, count)