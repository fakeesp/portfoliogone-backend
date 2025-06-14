from decimal import ROUND_DOWN, Decimal


def round_decimal(value: Decimal, precision: int = 9) -> Decimal:
    return value.quantize(Decimal(f".{'0' * precision}"), rounding=ROUND_DOWN).normalize()
