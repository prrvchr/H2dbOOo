#!
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020-25 https://prrvchr.github.io                                  ║
║                                                                                    ║
║   Permission is hereby granted, free of charge, to any person obtaining            ║
║   a copy of this software and associated documentation files (the "Software"),     ║
║   to deal in the Software without restriction, including without limitation        ║
║   the rights to use, copy, modify, merge, publish, distribute, sublicense,         ║
║   and/or sell copies of the Software, and to permit persons to whom the Software   ║
║   is furnished to do so, subject to the following conditions:                      ║
║                                                                                    ║
║   The above copyright notice and this permission notice shall be included in       ║
║   all copies or substantial portions of the Software.                              ║
║                                                                                    ║
║   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                  ║
║   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES                  ║
║   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.        ║
║   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY             ║
║   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,             ║
║   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE       ║
║   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                    ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
"""

from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from .optionsmodel import OptionsModel
from .optionsview import OptionsView

from ..unotool import getDesktop

from ..logger import LogManager

from ..configuration import g_defaultlog
from ..configuration import g_synclog


class OptionsManager():
    def __init__(self, ctx, logger, window, offset=0):
        self._ctx = ctx
        self._logger = logger
        self._model = OptionsModel(ctx)
        self._view = OptionsView(window, OptionsManager._restart, offset, *self._model.getViewData())
        self._logmanager = LogManager(self._ctx, window, 'requirements.txt', g_defaultlog, g_synclog)
        self._logmanager.initView()
        self._logger.logprb(INFO, 'OptionsManager', '__init__()', 301)
        self._model.loadDriver()

    _restart = False

    def loadSetting(self):
        self._view.setTimeout(self._model.getTimeout())
        self._view.setViewName(self._model.getViewName())
        self._view.setRestart(OptionsManager._restart)
        self._logmanager.loadSetting()
        self._logger.logprb(INFO, 'OptionsManager', 'loadSetting()', 311)

    def saveSetting(self):
        timeout, view = self._view.getViewData()
        option = self._model.setViewData(timeout, view)
        log = self._logmanager.saveSetting()
        if log:
            OptionsManager._restart = True
            self._view.setRestart(True)
        self._logger.logprb(INFO, 'OptionsManager', 'saveSetting()', 321, option, log)

    def viewData(self):
        url = self._model.getDatasourceUrl()
        getDesktop(self._ctx).loadComponentFromURL(url, '_default', 0, ())

