import re
from typing import Tuple, List, Dict

# Patrones ordenados de más específico a más genérico.
# El orden importa: cada patrón se aplica sobre el texto ya enmascarado por el anterior.
SECRET_PATTERNS: List[Tuple[str, str, re.Pattern]] = [
    (
        "AWS Access Key",
        "[REDACTED_AWS_KEY]",
        re.compile(r'\b(AKIA[0-9A-Z]{16})\b'),
    ),
    (
        "OpenAI API Key",
        "[REDACTED_OPENAI_KEY]",
        re.compile(r'\b(sk-(?:proj-)?[a-zA-Z0-9\-_]{20,})\b'),
    ),
    # GitHub / GitLab token raw values — must come BEFORE the generic password pattern
    (
        "GitHub Token",
        "[REDACTED_GITHUB_TOKEN]",
        re.compile(r'\b(gh[pousr]_[a-zA-Z0-9]{36,}|github_pat_[a-zA-Z0-9_]{20,})\b'),
    ),
    (
        "JWT Token",
        "[REDACTED_JWT_TOKEN]",
        re.compile(r'\b(eyJ[a-zA-Z0-9_\-]{10,}\.eyJ[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{10,})\b'),
    ),
    (
        "Private Key",
        "[REDACTED_PRIVATE_KEY]",
        re.compile(r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----[\s\S]*?-----END\s+(?:RSA\s+)?PRIVATE\s+KEY-----'),
    ),
    (
        "Hardcoded Password",
        "[REDACTED_PASSWORD]",
        # Negative lookahead: do not match values already containing [REDACTED_ placeholders
        re.compile(r'(?i)(?:password|passwd|pwd|secret|api_key|token)\s*[:=]\s*["\'](?!\[REDACTED_)([^"\']{6,})["\']'),
    ),
]


class SecretMasker:
    """Detecta y enmascara credenciales y secretos sensibles en el código antes de la evaluación LLM."""

    def mask_secrets(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        """
        Escanea el texto en busca de patrones de secretos.
        Aplica los patrones secuencialmente — cada uno opera sobre el texto ya enmascarado.
        Retorna:
            - masked_text: Texto con los secretos reemplazados por placeholders de seguridad.
            - detections: Lista de secretos detectados y su categoría.
        """
        masked_text = text
        detections: List[Dict[str, str]] = []

        for name, replacement, pattern in SECRET_PATTERNS:
            # Detectar coincidencias en el texto actual (ya parcialmente enmascarado)
            for match in pattern.finditer(masked_text):
                matched_val = match.group(1) if match.groups() else match.group(0)
                detections.append({
                    "type": name,
                    "sample": matched_val[:4] + "****",
                })

            # Aplicar enmascaramiento
            if pattern.groups >= 1:
                # Reemplazar solo el grupo capturado (el valor secreto), preservando el contexto
                masked_text = pattern.sub(
                    lambda m, r=replacement: m.group(0).replace(m.group(1), r),
                    masked_text,
                )
            else:
                masked_text = pattern.sub(replacement, masked_text)

        return masked_text, detections
