import re
from typing import Tuple, Optional


class DomainIntentGuard:
    """
    Guardrail de seguridad semántico y clasificador determinista de intención de dominio
    para mitigar vulnerabilidades OWASP LLM01 (Prompt Injection & Jailbreak),
    OWASP LLM06 (Excessive Agency / Fuera de Dominio) y OWASP LLM04 (DoS por inferencia).
    """

    # Patrones de ataque de Prompt Injection / Jailbreaking
    JAILBREAK_PATTERNS = [
        r'(?i)\b(?:ignora|olvida|descarta)\s+(?:todas\s+las\s+)?(?:tus\s+)?(?:instrucciones|directivas|reglas)\b',
        r'(?i)\b(?:ignore|forget|disregard)\s+(?:all\s+)?(?:previous\s+)?(?:instructions|rules|system\s+prompt)\b',
        r'(?i)\b(?:act[uú]a\s+como|pretend\s+to\s+be|roleplay\s+as)\s+(?:un\s+)?(?:dan|hacker|amigo|psic[oó]logo|terapeuta|poeta)\b',
        r'(?i)\b(?:system\s+override|jailbreak|developer\s+mode|modo\s+desarrollador)\b',
        r'(?i)\b(?:modo\s+sin\s+censura|unfiltered\s+mode|bypass\s+safety)\b',
    ]

    # Patrones explícitos de insultos y hostilidad
    ABUSIVE_PATTERNS = [
        r'(?i)\b(?:insult(?:[a-zñáéíóú]+)?|ofend(?:[a-zñáéíóú]+)?|ofensas?|agred(?:[a-zñáéíóú]+)?|maldici[oó]n|groser[ií]as?)\b',
        r'(?i)\b(?:insult\s+me|swear\s+at\s+me|abusive\s+language)\b',
    ]

    # Patrones de consultas comunes fuera del dominio de ingeniería de software
    OUT_OF_SCOPE_PATTERNS = [
        # Operaciones matemáticas (aisladas o mencionadas en la frase)
        r'[-+]?\d+\s*[\+\-\*\/\^x×÷]\s*[-+]?\d+(?:\s*[\+\-\*\/\^x×÷]\s*[-+]?\d+)*',
        r'(?i)\b(?:cu[aá]nto\s+es|resuelve\s+esta\s+operaci[oó]n|calcula)\b',
        # Asesoría personal, emocional o médica
        r'(?i)\b(?:me\s+siento\s+(?:mal|triste|deprimido|solo|ansioso)|se\s+siente\s+mal)\b',
        r'(?i)\b(?:psic[oó]log(?:o|a)|terapia\s+emocional|dolor\s+emocional|depresi[oó]n|autoayuda)\b',
        # Tareas ajenas a código (recetas, poesía, clima, etc.)
        r'(?i)\b(?:receta\s+de\s+cocina|poema|escribe\s+un\s+cuento|el\s+clima\s+en|noticias\s+de)\b',
    ]

    # Lista positiva: términos representativos del dominio de Praxia
    DOMAIN_KEYWORDS = [
        'código', 'codigo', 'code', 'software', 'arquitectura', 'architecture',
        'refactor', 'refactorizar', 'función', 'funcion', 'function', 'método', 'metodo', 'method',
        'clase', 'class', 'solid', 'clean code', 'srp', 'ocp', 'lsp', 'isp', 'dip',
        'complejidad', 'mantenibilidad', 'maintainability', 'ciclomática', 'cyclomatic',
        'dependencia', 'dependency', 'ciclo', 'cycle', 'adp', 'dora', 'test', 'prueba',
        'duplicación', 'duplicacion', 'finding', 'hallazgo', 'ast', 'árbol', 'arbol',
        'vulnerabilidad', 'seguridad', 'security', 'owasp', 'token', 'auth', 'api',
        'repositorio', 'repo', 'commit', 'branch', 'rama', 'pull request', 'pr',
        'backend', 'frontend', 'patrón', 'patron', 'pattern', 'acoplamiento', 'cohesión', 'cohesion'
    ]

    STANDARD_REJECTION_MESSAGE = (
        "Praxia es un sistema exclusivo de auditoría de arquitectura y calidad de código de software. "
        "No tengo autorización para participar en interacciones personales, insultos, operaciones no relacionadas "
        "o temas fuera del ámbito de ingeniería de software de este repositorio."
    )

    @classmethod
    def evaluate_query(cls, query: str) -> Tuple[bool, Optional[str]]:
        """
        Evalúa la consulta del usuario.
        Retorna:
            - is_allowed: True si la consulta es pertinente al dominio o segura; False si debe ser rechazada.
            - rejection_message: Mensaje explicativo de rechazo inmediato si is_allowed es False, o None.
        """
        trimmed = query.strip()
        if not trimmed:
            return True, None

        # 1. Comprobar intentos de Jailbreak / Prompt Injection
        for pat in cls.JAILBREAK_PATTERNS:
            if re.search(pat, trimmed):
                return False, (
                    "Solicitud rechazada bajo política de seguridad OWASP LLM01: Se ha detectado un intento "
                    "de alterar las directivas del sistema o evadir las restricciones de dominio de Praxia."
                )

        # 2. Comprobar peticiones de insultos o lenguaje hostil
        for pat in cls.ABUSIVE_PATTERNS:
            if re.search(pat, trimmed):
                return False, (
                    "Praxia está diseñado exclusivamente para auditoría técnica de software y revisión de código. "
                    "No participo en la generación de insultos, lenguaje abusivo o descalificaciones personales."
                )

        # 3. Comprobar consultas explícitamente fuera de ámbito (matemáticas elementales, apoyo emocional, etc.)
        for pat in cls.OUT_OF_SCOPE_PATTERNS:
            if re.search(pat, trimmed):
                return False, cls.STANDARD_REJECTION_MESSAGE

        # 4. Si la consulta es corta (<= 5 palabras) y contiene únicamente palabras off-topic
        words = [w.lower() for w in re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9_-]+\b', trimmed)]
        if len(words) <= 4:
            has_domain_word = any(w in cls.DOMAIN_KEYWORDS for w in words)
            greeting_words = {'hola', 'buenas', 'hello', 'hi', 'ayuda', 'help', 'status', 'info'}
            is_greeting = any(w in greeting_words for w in words)
            
            # Consultas como "insultame", "cantame", "2x2", "cuentame un chiste"
            chitchat_block = {'insultame', 'insulto', 'broma', 'chiste', 'canta', 'poema', 'hermano'}
            if any(w in chitchat_block for w in words) and not has_domain_word:
                return False, cls.STANDARD_REJECTION_MESSAGE

        return True, None
