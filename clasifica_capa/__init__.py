# -*- coding: utf-8 -*-
"""
/***************************************************************************
 clasifica
                                 A QGIS plugin
 esto es para una segunda prueba
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-07-08
        copyright            : (C) 2020 by Víctor Hernandez
        email                : victorhdzgeo@gmail.com
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
    """Load clasifica class from file clasifica.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .clasifica_capa import clasifica
    return clasifica(iface)
