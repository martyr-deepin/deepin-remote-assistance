
import gettext
from .constants import APP_SNAME
from .constants import LOCALE_DIR

gettext.bindtextdomain(APP_SNAME, LOCALE_DIR)
gettext.textdomain(APP_SNAME)
_ = gettext.gettext

__all__ = ['_', ]
