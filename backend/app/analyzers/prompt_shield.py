import re
from typing import Optional


def sanitize_code_delimiter(code: str) -> str:
    """
    Sanitiza el código fuente para prevenir ataques de prompt injection
    destinados a cerrar prematuramente los delimitadores XML o Markdown.
    Escapa ocurrencias literales de etiquetas delimitadoras como </untrusted_source_code>.
    """
    if not code:
        return ""
    # Neutralizar etiquetas de cierre simuladas dentro de cadenas o comentarios
    sanitized = re.sub(
        r'<\s*/\s*untrusted_source_code\s*>',
        '[ESCAPED_UNTRUSTED_DELIMITER_CLOSE]',
        code,
        flags=re.IGNORECASE
    )
    sanitized = re.sub(
        r'<\s*untrusted_source_code(?:\s+[^>]*)?>',
        '[ESCAPED_UNTRUSTED_DELIMITER_OPEN]',
        sanitized,
        flags=re.IGNORECASE
    )
    return sanitized


def wrap_untrusted_code(code: str, file_path: str = "unknown", language: str = "") -> str:
    """
    Encapsula de forma estricta cualquier código fuente de usuario dentro de etiquetas
    delimitadoras XML estandarizadas recomendadas por OWASP LLM01.
    """
    safe_code = sanitize_code_delimiter(code)
    lang_attr = f' language="{language}"' if language else ""
    return (
        f'<untrusted_source_code file="{file_path}"{lang_attr}>\n'
        f'{safe_code}\n'
        f'</untrusted_source_code>'
    )
