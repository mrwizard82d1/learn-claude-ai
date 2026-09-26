def add(numbers):
    if not numbers:
        return 0
    return sum(int(x) for x in numbers.split(","))
