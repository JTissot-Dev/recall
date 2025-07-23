from datetime import datetime, timezone
from typing import Optional


def utc_now() -> datetime:
    """Retourne le datetime UTC actuel."""
    return datetime.now(timezone.utc)


def utc_timestamp() -> float:
    """Retourne le timestamp UTC actuel."""
    return datetime.now(timezone.utc).timestamp()


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Formate un datetime en string."""
    return dt.strftime(fmt)


def parse_datetime(
    date_string: Optional[str], 
    fmt: Optional[str] = None
) -> Optional[datetime]:
    """
    Parse une string en datetime avec support robuste des formats ISO.
    
    Args:
        date_string: String à parser (peut être None)
        fmt: Format spécifique (si None, utilise auto-détection ISO)
    
    Returns:
        datetime object ou None si date_string est None/vide
        
    Raises:
        ValueError: Si le format n'est pas supporté
        
    Examples:
        parse_datetime("2025-07-08T15:32:18")           # ISO basique
        parse_datetime("2025-07-08T15:32:18.823224")    # ISO avec microsecondes
        parse_datetime("2025-07-08T15:32:18Z")          # ISO avec timezone Z
        parse_datetime("2025-07-08T15:32:18+02:00")     # ISO avec timezone
        parse_datetime("2025-07-08 15:32:18", "%Y-%m-%d %H:%M:%S")  # Format custom
    """
    if not date_string:
        return None
    
    # ✅ Si format spécifique fourni, l'utiliser directement
    if fmt:
        return datetime.strptime(date_string, fmt)
    
    # ✅ Auto-détection ISO avec fallbacks multiples
    # Normaliser la string (gérer timezone Z)
    normalized_string = date_string.replace('Z', '+00:00')
    
    # ✅ Essayer fromisoformat en premier (plus rapide et robuste)
    try:
        return datetime.fromisoformat(normalized_string)
    except ValueError:
        pass
    
    # ✅ Formats de fallback courants
    iso_formats = [
        "%Y-%m-%dT%H:%M:%S.%f",        # 2025-07-08T15:32:18.823224
        "%Y-%m-%dT%H:%M:%S",           # 2025-07-08T15:32:18
        "%Y-%m-%dT%H:%M:%S.%fZ",       # 2025-07-08T15:32:18.823224Z
        "%Y-%m-%dT%H:%M:%SZ",          # 2025-07-08T15:32:18Z
        "%Y-%m-%d %H:%M:%S.%f",        # 2025-07-08 15:32:18.823224
        "%Y-%m-%d %H:%M:%S",           # 2025-07-08 15:32:18
        "%Y-%m-%dT%H:%M:%S%z",         # 2025-07-08T15:32:18+02:00
        "%Y-%m-%dT%H:%M:%S.%f%z",      # 2025-07-08T15:32:18.823224+02:00
    ]
    
    # ✅ Essayer chaque format
    for fmt_pattern in iso_formats:
        try:
            return datetime.strptime(date_string, fmt_pattern)
        except ValueError:
            continue
    
    # ❌ Aucun format ne marche
    raise ValueError(
        f"Unable to parse datetime '{date_string}'. "
        f"Supported formats: ISO 8601 (e.g., 2025-07-08T15:32:18 or 2025-07-08T15:32:18.823224) "
        f"or specify custom format with fmt parameter."
    )


def to_utc(dt: datetime) -> datetime:
    """Convertit un datetime en UTC."""
    if dt.tzinfo is None:
        # Assume local timezone if naive
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
