"""
Sample domain module intentionally violating hexagonal architecture rules
by importing from an API endpoint directly.
"""
from app.api.v1.endpoints.sonar import get_sonar_topography


class DomainSampleEntity:
    def __init__(self, name: str):
        self.name = name

    def compute_risk(self) -> dict:
        return get_sonar_topography()
