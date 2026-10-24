from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.entities import ChatSession, Repo
from app.schemas.api import ChatSessionItem, ChatSessionDetail, ChatSessionCreate

router = APIRouter()


@router.get("/", response_model=List[ChatSessionItem], summary="Listar sesiones previas")
def list_chat_sessions(
    repo_id: Optional[str] = Query(None, description="Filtrar sesiones por repositorio"),
    source: Optional[str] = Query(None, description="Filtrar por origen (cli o web)"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Retorna el historial de sesiones de conversación guardadas para poder
    remontarse a ellas (/resume), similar a la experiencia en AGY.
    """
    q = db.query(ChatSession)
    if repo_id:
        q = q.filter(ChatSession.repo_id == repo_id)
    if source:
        q = q.filter(ChatSession.source == source)

    sessions = q.order_by(desc(ChatSession.updated_at)).limit(limit).all()
    results = []
    for s in sessions:
        results.append(ChatSessionItem(
            id=s.id,
            repo_id=s.repo_id,
            title=s.title,
            source=s.source,
            model=s.model,
            tier=s.tier,
            messages_count=len(s.messages) if isinstance(s.messages, list) else 0,
            created_at=s.created_at,
            updated_at=s.updated_at,
        ))
    return results


@router.get("/{session_id}", response_model=ChatSessionDetail, summary="Obtener detalle y mensajes de una sesión")
def get_chat_session(session_id: str, db: Session = Depends(get_db)):
    """Obtiene los mensajes y el contexto completo de una sesión para reanudarla."""
    session_obj = db.query(ChatSession).filter_by(id=session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    return ChatSessionDetail(
        id=session_obj.id,
        repo_id=session_obj.repo_id,
        title=session_obj.title,
        source=session_obj.source,
        model=session_obj.model,
        tier=session_obj.tier,
        messages=session_obj.messages if isinstance(session_obj.messages, list) else [],
        created_at=session_obj.created_at,
        updated_at=session_obj.updated_at,
    )


@router.post("/", response_model=ChatSessionDetail, summary="Guardar o actualizar una sesión")
def save_chat_session(payload: ChatSessionCreate, db: Session = Depends(get_db)):
    """Crea una nueva sesión de chat o guarda el progreso de la conversación."""
    new_sess = ChatSession(
        repo_id=payload.repo_id,
        title=payload.title,
        source=payload.source,
        model=payload.model,
        tier=payload.tier,
        messages=payload.messages,
    )
    db.add(new_sess)
    db.commit()
    db.refresh(new_sess)
    return ChatSessionDetail(
        id=new_sess.id,
        repo_id=new_sess.repo_id,
        title=new_sess.title,
        source=new_sess.source,
        model=new_sess.model,
        tier=new_sess.tier,
        messages=new_sess.messages if isinstance(new_sess.messages, list) else [],
        created_at=new_sess.created_at,
        updated_at=new_sess.updated_at,
    )


@router.put("/{session_id}", response_model=ChatSessionDetail, summary="Actualizar mensajes de una sesión")
def update_chat_session(session_id: str, payload: ChatSessionCreate, db: Session = Depends(get_db)):
    """Actualiza una sesión existente agregando nuevos mensajes."""
    session_obj = db.query(ChatSession).filter_by(id=session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    if payload.title:
        session_obj.title = payload.title
    session_obj.messages = payload.messages
    session_obj.model = payload.model
    session_obj.tier = payload.tier
    db.commit()
    db.refresh(session_obj)

    return ChatSessionDetail(
        id=session_obj.id,
        repo_id=session_obj.repo_id,
        title=session_obj.title,
        source=session_obj.source,
        model=session_obj.model,
        tier=session_obj.tier,
        messages=session_obj.messages if isinstance(session_obj.messages, list) else [],
        created_at=session_obj.created_at,
        updated_at=session_obj.updated_at,
    )


@router.delete("/{session_id}", summary="Eliminar una sesión")
def delete_chat_session(session_id: str, db: Session = Depends(get_db)):
    session_obj = db.query(ChatSession).filter_by(id=session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    db.delete(session_obj)
    db.commit()
    return {"success": True, "message": "Sesión eliminada correctamente", "id": session_id}
