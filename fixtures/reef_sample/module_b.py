"""
Sample module B for circular dependency demonstration.
"""
from fixtures.reef_sample.module_c import process_c


def process_b() -> str:
    return f"B -> {process_c()}"
