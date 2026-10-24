try:
    from app.agents.graph import opennavy_graph, praxia_graph, build_analysis_graph
except ImportError:
    opennavy_graph = None
    praxia_graph = None
    build_analysis_graph = None

__all__ = [
    "opennavy_graph",
    "praxia_graph",
    "build_analysis_graph",
]
