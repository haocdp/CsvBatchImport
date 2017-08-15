# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CsvBatchImport
                                 A QGIS plugin
 Batch Import .csv Files in a Dictionary 
                             -------------------
        begin                : 2017-08-09
        copyright            : (C) 2017 by haoc
        email                : haoc_dp@163.com
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
    """Load CsvBatchImport class from file CsvBatchImport.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .csv_batch_import import CsvBatchImport
    return CsvBatchImport(iface)
