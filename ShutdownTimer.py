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
version = "0.2"
creator = "Triangle717"

def main():
    '''Main Menu'''
    sys.stdout.write("\n{0} {1}, Copyright 2013 {2}\n".format(app, version, creator))
    sys.stdout.write("\nPlease enter the time you want the computer to shutdown.\n")
    sys.stdout.write("Hint: Use the 12 hour format, with the following layout: 'HH:MM'")
    offtime = get_input("\n\n> ")
    time.sleep(50)
    raise SystemExit
##sys.stdout.write("Shutdown started")
##time.sleep(offtime)
##sys.stdout.write("os.system('shutdown /r /t 0')")
##sys.stdout.write("Shutting down PC...")
##os.system("shutdown /r /t 0")


def one2tot24(offtime):
    '''Converts 12-hour format to 24-hour format'''

    # The current time, as defined by the System Clock
    cur_time = strftime("%H:%M %p", localtime())


# -- Resource links just for me. :) -- #

#http://www.dreamincode.net/forums/topic/210175-shutting-down-a-computer-from-python/
#http://www.computerperformance.co.uk/windows7/windows7_shutdown_command.htm
#http://www.thewindowsclub.com/shutdown-restart-windows-8

if __name__ == "__main__":
    if sys.version_info >= (3,0):
        # Use Python 3 input
        get_input = input
        main()
    else:
        # Use Python 2 input
        get_input = raw_input
        main()