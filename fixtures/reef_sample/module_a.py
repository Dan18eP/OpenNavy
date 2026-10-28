"""
Sample module A for circular dependency demonstration.
"""
from fixtures.reef_sample.module_b import process_b


def process_a() -> str:
    return f"A -> {process_b()}"
