
import QtQuick 2.2

import Deepin.Widgets 1.0

DMenu {
    DMenuItem {
        label: dsTr("Optimize Performance")
    }

    DMenuItem {
        label: dsTr("Optimize Quality")
    }

    DMenuItem {
        label: dsTr("Balance")
    }

    DMenuSeparator {
    }

    DToggleMenuItem {
        label: dsTr("Fullscreen")
    }
}
