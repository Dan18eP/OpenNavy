"""
Sample module C for circular dependency demonstration.
Completes the cycle: module_a -> module_b -> module_c -> module_a.
"""
from fixtures.reef_sample.module_a import process_a


def process_c() -> str:
    return f"C -> {process_a()}"
