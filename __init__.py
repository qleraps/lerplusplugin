# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LerPlusDock
                                 A QGIS plugin
 Nem adgang til LER2 forespørgsler
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-10-09
        copyright            : (C) 2023 by qLER ApS
        email                : morten@qler.dk
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load LerPlusDock class from file LerPlusDock.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .lerplusdock import LerPlusDock
    plugin = LerPlusDock(iface)

    # This will make sure that the plugin is cleaned up properly
    try:
        plugin.unload()
    except Exception as e:
        pass

    return plugin
