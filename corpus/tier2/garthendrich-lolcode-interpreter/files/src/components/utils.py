def isEmpty(body):
    return len(body) == 0


def toNumber(value):
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return float(value)
    return value
