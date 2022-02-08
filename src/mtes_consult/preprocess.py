"""Prétraitement du fichier brut contenant les commentaires.
"""
import logging
import os

from . import _

_logger = logging.getLogger(__name__)


def preprocess(consultation: str, data_dir: os.PathLike) -> None:
    _logger.info("Prétraitement de %s", consultation)

    return None
