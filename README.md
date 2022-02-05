# mtes_consult

Téléchargement et analyse de consultations publiques du ministère de la Transition écologique

## Description

A faire...

## Installation

Pour installer l'environnement:

## Utilisation

1. Téléchargement d'une consultation:
   ```
   cd scraper
   editor mte/spiders/mte_crawler.py  # Modifier start_urls pour pointer sur la consultation
   scrapy crawl mte_crawler --overwrite-output=../data/raw/nom_consultation.csv --logfile=$HOME/tmp/nom_consultation.log --loglevel=INFO
   ```

2. Traitement d'une consultation
   ```
   python -m ana_consult.mtes_analyze --prep .mtes.yaml
   ```
