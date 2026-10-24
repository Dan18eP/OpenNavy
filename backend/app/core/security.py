import hmac
import hashlib
import logging
from typing import Optional
from fastapi import HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)


def verify_github_signature(raw_body: bytes, signature_header: Optional[str]) -> bool:
    """
    Valida criptográficamente la cabecera X-Hub-Signature-256 de GitHub usando HMAC-SHA256.
    Si WEBHOOK_SECRET está configurado y la firma falta o no coincide, lanza HTTPException 401.
    """
    secret = settings.WEBHOOK_SECRET
    if not secret:
        # Modo permisivo si no hay secreto configurado en el entorno
        return True

    if not signature_header:
        logger.warning("Intento de webhook de GitHub sin cabecera X-Hub-Signature-256")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firma de GitHub requerida (X-Hub-Signature-256 faltante)."
        )

    if not signature_header.startswith("sha256="):
        logger.warning(f"Formato de firma no soportado: {signature_header}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de firma inválido (se esperaba sha256=...)."
        )

    expected_signature = signature_header[len("sha256="):]
    computed_signature = hmac.new(
        key=secret.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed_signature, expected_signature):
        logger.warning("Firma HMAC-SHA256 de GitHub inválida")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firma criptográfica inválida para el webhook de GitHub."
        )

    return True


def verify_gitlab_token(token_header: Optional[str]) -> bool:
    """
    Valida la cabecera X-Gitlab-Token de GitLab comparándola de forma segura contra GITLAB_WEBHOOK_TOKEN.
    Si GITLAB_WEBHOOK_TOKEN está configurado y el token no coincide, lanza HTTPException 401.
    """
    expected_token = settings.GITLAB_WEBHOOK_TOKEN
    if not expected_token:
        # Modo permisivo si no hay secreto configurado en el entorno
        return True

    if not token_header:
        logger.warning("Intento de webhook de GitLab sin cabecera X-Gitlab-Token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token secreto de GitLab requerido (X-Gitlab-Token faltante)."
        )

    if not hmac.compare_digest(token_header, expected_token):
        logger.warning("Token de GitLab inválido")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de webhook de GitLab inválido."
        )

    return True
