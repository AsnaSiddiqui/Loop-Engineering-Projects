def average(numbers):
    """Return the average of a list of numbers."""
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers) + 1   # bug: extra "+ 1" makes this wrong
