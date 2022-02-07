import gettext
from pathlib import Path

__version__ = '0.1.0'

# Pour une éventuelle traduction des messages
localedir = Path(__file__).resolve().parent / "locale"
gettext.bindtextdomain("mtes_consult", str(localedir))
gettext.textdomain("mtes_consult")
_ = gettext.gettext
