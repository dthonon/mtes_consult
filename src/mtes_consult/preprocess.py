"""Prétraitement du fichier brut contenant les commentaires.
"""
import csv
import hashlib
import logging
import os
from pathlib import Path

import pandas as pd

from . import _

_logger = logging.getLogger(__name__)


def preprocess(consultation: str, data_dir: os.PathLike) -> None:
    _logger.info("Prétraitement de %s", consultation)
    csv_file = data_dir + "/raw/" + consultation + ".csv"
    _logger.debug(_("Lecture %s"), csv_file)
    responses = pd.read_csv(csv_file, header=0, quoting=csv.QUOTE_ALL, nrows=1000000)
    _logger.info(_("Nombre de commentaires bruts : %d"), len(responses))

    # Ajout hash-key pour assurer la traçabilité en cours de traitement
    responses["uid"] = responses.sujet.apply(
        lambda t: hashlib.sha224(t.encode("utf-8")).hexdigest()
    )

    # Découpe du sujet en éléments
    responses[["titre", "nom", "date", "heure"]] = responses.sujet.str.extract(
        "(.*), par  (.*) ,, le (.*) à (.*)", expand=True
    )
    responses = responses.drop(columns=["sujet"])
    responses = responses[
        ["titre", "nom", "date", "heure", "texte", "uid"]
    ].sort_values(by="nom", ignore_index=True)

    # Suppression des ligne dupliquées
    # responses.drop_duplicates(subset=["nom", "titre"], inplace=True)
    # responses = responses.drop_duplicates(subset=["nom", "texte"])
    _logger.info(_("Commentaires restants après déduplication : %d"), len(responses))

    print(responses.head(10))
    csv_file = data_dir + "/preprocessed/" + consultation + ".csv"
    _logger.debug(_("Ecriture dans %s"), csv_file)
    responses.to_csv(csv_file, header=0, quoting=csv.QUOTE_ALL)

    return None
