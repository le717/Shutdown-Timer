#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shutdown Timer -  Small Windows shutdown timer.

Created 2013, 2015 Triangle717
<http://Triangle717.WordPress.com>

Shutdown Timer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Shutdown Timer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Shutdown Timer. If not, see <http://www.gnu.org/licenses/>.

"""
import os
import sys
from cx_Freeze import (setup, Executable)

import constants as const


# Windows
if sys.platform == "win32":

    # x86 build
    if sys.maxsize < 2 ** 32:
        destfolder = os.path.join("bin", "Windows", "x86")

        # x64 build
    else:
        destfolder = os.path.join("bin", "Windows", "x64")
        
else:
    print("{0} is not supported on non Windows OS!".format(const.appName))
    raise SystemExit(0)

# Create the freeze path if it doesn't exist
if not os.path.exists(destfolder):
    os.makedirs(destfolder)

build_exe_options = {
    "build_exe": destfolder,
     "create_shared_zip": True,
     "optimize": 1,
     "compressed": True,
     "icon": "Icon.ico"
}

setup(
    name=const.appName,
    version=const.version,
    author=const.creator,
    description="{0} v{1}".format(const.appName, const.version),
    license="GPL v3",
    options={"build_exe": build_exe_options},
    executables=[Executable("ShutdownTimer.py")])
