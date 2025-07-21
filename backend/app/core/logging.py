import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from app.core.config import settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Configure logging for the application.

    Args:
        log_level: Override log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Déterminer le niveau de log
    if log_level:
        level = getattr(logging, log_level.upper())
    else:
        level = logging.DEBUG if settings.APP_ENV == "dev" else logging.INFO

    # Créer le dossier logs (relatif à la racine backend)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Format détaillé pour les logs
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )

    # Format simple pour la console
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Supprimer les handlers existants
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 1. ✅ Handler CONSOLE
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)

    # 2. ✅ Handler APPLICATION générale
    app_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=50 * 1024 * 1024,  # 50MB
        backupCount=10,
        encoding="utf-8",
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(detailed_formatter)

    # 3. ✅ Handler ERREURS seulement
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / "errors.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)

    # 4. ✅ Handler CHAT spécifique
    chat_handler = logging.handlers.RotatingFileHandler(
        log_dir / "chat.log",
        maxBytes=20 * 1024 * 1024,  # 20MB
        backupCount=7,
        encoding="utf-8",
    )
    chat_handler.setLevel(logging.DEBUG)
    chat_handler.setFormatter(detailed_formatter)

    # Configuration du root logger
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)

    # Logger spécifique pour le ChatService
    chat_logger = logging.getLogger("app.services.chat_service")
    chat_logger.addHandler(chat_handler)
    chat_logger.setLevel(logging.DEBUG)

    # Réduire le bruit des librairies externes
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    # Log de confirmation
    logger = logging.getLogger(__name__)
    logger.info(
        f"Logging configured - Level: {logging.getLevelName(level)} - Environment: {settings.APP_ENV}"
    )
    logger.info(f"Log directory: {log_dir.absolute()}")
