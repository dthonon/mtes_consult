#!/usr/bin/env python3
"""
Analyse des commentaires à une consultation.
"""
import argparse
import logging
import sys
import os

from . import _, __version__
from .preprocess import preprocess

_logger = logging.getLogger()


class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError(
                "readable_dir:{0} is not a valid path".format(prospective_dir)
            )
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentTypeError(
                "readable_dir:{0} is not a readable dir".format(prospective_dir)
            )


def arguments(args):
    """Define and parse command arguments.

    Args:
        args ([str]): command line parameters as list of strings

    Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """
    # Get options
    parser = argparse.ArgumentParser(
        description="Analyse des commentaires d'une consultation MTE."
    )
    parser.add_argument(
        "--version",
        help=_("Imprime le numéro de version"),
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    out_group = parser.add_mutually_exclusive_group()
    out_group.add_argument(
        "--verbose", help=_("Traces plus verbeuses (DEBUG)"), action="store_true"
    )
    out_group.add_argument(
        "--quiet", help=_("Traces moins verbeuses (WARNING)"), action="store_true"
    )
    parser.add_argument(
        "--data_directory",
        help=_("Répertoire contenant les répertoires de données raw, preprocessed..."),
        required=True,
        action=readable_dir,
    )
    parser.add_argument(
        "--consultation",
        help=_("Nom de la consultation, qui permet de nommer les fichiers"),
        required=True,
        type=str,
    )
    parser.add_argument(
        "--preprocess",
        help=_("Charge le fichier CSV brut et effectue les pré-traitements"),
        action="store_true",
    )

    return parser.parse_args(args)


def setup(args):
    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    ch.setFormatter(formatter)
    # add the handlers to the logger
    _logger.addHandler(ch)

    # Define verbosity
    if args.verbose:
        _logger.setLevel(logging.DEBUG)
    else:
        _logger.setLevel(logging.INFO)
    return


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    # Arguments d'appel
    args = arguments(args)

    # Mise en place de l'environnement
    setup(args)

    _logger.info(_("%s, version %s"), sys.argv[0], __version__)
    _logger.info(_("Arguments: %s"), sys.argv[1:])

    # Preprocess csv file
    if args.preprocess:
        preprocess(args.consultation, args.data_directory)

    _logger.info(_("Fin du traitement"))
    return None


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


# Main wrapper
if __name__ == "__main__":
    run()
