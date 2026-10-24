from typing import Dict, Any
from langgraph.graph import StateGraph, END
from app.schemas.state import AnalysisState
from app.agents.nodes import (
    clone_node,
    static_analysis_node,
    architecture_inference_node,
    rag_retrieval_node,
    llm_evaluator_node,
    docs_generator_node,
    persist_node,
    offline_synthesizer_node,
)


def should_continue_after_step(state: AnalysisState) -> str:
    """Verifica si hubo un error crítico para saltar directo a persistencia."""
    errors = state.get("errors", [])
    if errors or state.get("current_step") == "failed":
        return "persist"
    return "continue"


def route_evaluation_or_offline(state: AnalysisState) -> str:
    """
    Circuit Breaker (HU-CORE-03):
    Evalúa si se debe enrutar hacia la evaluación con LLM o hacia el sintetizador determinístico offline.
    """
    if state.get("offline_mode") is True:
        return "offline"

    # Verificar disponibilidad rápida de LLM
    try:
        from app.core.llm import get_llm
        llm = get_llm()
        if not llm:
            return "offline"
    except Exception:
        return "offline"

    return "llm"


def build_analysis_graph():
    """Construye y compila el grafo de orquestación de análisis en LangGraph con Circuit Breaker."""
    workflow = StateGraph(AnalysisState)

    # 1. Agregar Nodos
    workflow.add_node("clone", clone_node)
    workflow.add_node("static_analysis", static_analysis_node)
    workflow.add_node("architecture_inference", architecture_inference_node)
    workflow.add_node("rag_retrieval", rag_retrieval_node)
    workflow.add_node("llm_evaluator", llm_evaluator_node)
    workflow.add_node("offline_synthesizer", offline_synthesizer_node)
    workflow.add_node("docs_generator", docs_generator_node)
    workflow.add_node("persist", persist_node)

    # 2. Configurar Punto de Entrada
    workflow.set_entry_point("clone")

    # 3. Configurar Aristas y Transiciones Condicionales
    workflow.add_conditional_edges(
        "clone",
        should_continue_after_step,
        {
            "continue": "static_analysis",
            "persist": "persist",
        }
    )

    workflow.add_conditional_edges(
        "static_analysis",
        should_continue_after_step,
        {
            "continue": "architecture_inference",
            "persist": "persist",
        }
    )

    workflow.add_conditional_edges(
        "architecture_inference",
        should_continue_after_step,
        {
            "continue": "rag_retrieval",
            "persist": "persist",
        }
    )

    # Arista condicional Circuit Breaker tras RAG Retrieval
    workflow.add_conditional_edges(
        "rag_retrieval",
        route_evaluation_or_offline,
        {
            "llm": "llm_evaluator",
            "offline": "offline_synthesizer",
        }
    )

    workflow.add_edge("llm_evaluator", "docs_generator")
    workflow.add_edge("offline_synthesizer", "docs_generator")
    workflow.add_edge("docs_generator", "persist")
    workflow.add_edge("persist", END)

    # 4. Compilar Grafo
    return workflow.compile()


# Grafo compilado listo para invocación
praxia_graph = build_analysis_graph()
