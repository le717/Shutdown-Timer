#! python3
"""
    Shutdown Timer -  Small Windows Shutdown Timer
    Created 2013 Triangle717 <http://triangle717.wordpress.com>

    Shutdown Timer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Shutdown Timer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Shutdown Timer.  If not, see <http://www.gnu.org/licenses/>.
"""

# Shutdown Timer setup script using cx_Freeze.
# Taken from https://github.com/Lyrositor/EBPatcher
# and https://github.com/JrMasterModelBuilder/JAM-Extractor
# With changes by Triangle717

from cx_Freeze import setup, Executable
import sys, platform

# Append build to the arguments. Just type "python setup.py" and it will compile
if len(sys.argv) == 1: sys.argv[1:] = ["build"]

# Compile into the proper folder depending on the architecture
# Based on code from the Python help file (platform module) and my own tests
if sys.maxsize == 2147483647:
    destfolder = "Compile/Windows32"
else:
    destfolder = "Compile/Windows64"

build_exe_options = {"build_exe": destfolder,
                     "create_shared_zip": True,
                     "optimize": 1,
                     "compressed": True}

setup(
    name = "Shutdown Timer",
    version = "1.0.2",
    author = "Triangle717",
    description = "Shutdown Timer Version 1.0.2, created 2013 Triangle717",
    license = "GNU GPLv3",
    options = {"build_exe": build_exe_options},
    executables = [Executable("ShutdownTimer.py")])
