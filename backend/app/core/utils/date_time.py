from datetime import datetime, timezone


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
    date_string: str, fmt: str = "%Y-%m-%d %H:%M:%S"
) -> datetime:
    """Parse une string en datetime."""
    return datetime.strptime(date_string, fmt)


def to_utc(dt: datetime) -> datetime:
    """Convertit un datetime en UTC."""
    if dt.tzinfo is None:
        # Assume local timezone if naive
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
