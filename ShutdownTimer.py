# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Shutdown Timer
# https://github.com/le717/Shutdown-Timer
# Copyright 2013 Triangle717 (http://triangle717.wordpress.com).


import sys, os, time

app = "Shutdown Timer"
version = "0.1"
creator = "Triangle717"

sys.stdout.write("{0} {1}, Copyright 2013 {2}".format(app, version, creator))
offtime = int(input("Please enter (using seconds) how long you wish to delay shutdown: "))
sys.stdout.write("Shutdown started")
time.sleep(offtime)
sys.stdout.write("os.system('shutdown /r /t 0')")
sys.stdout.write("Shutting down PC...")
os.system("shutdown /r /t 0")


# -- Resource links just for me. :) -- #

#http://www.dreamincode.net/forums/topic/210175-shutting-down-a-computer-from-python/
#http://www.computerperformance.co.uk/windows7/windows7_shutdown_command.htm
#http://www.thewindowsclub.com/shutdown-restart-windows-8

if __name__ == "__main__":
    if sys.versioninfo == (2,7,3):
        sys.stdout.write("Python 2.7")
    else:
        sys.stdout.write("Python 3")
