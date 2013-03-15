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


import sys, os
from time import strftime, localtime, sleep

app = "Shutdown Timer"
version = "0.3"
creator = "Triangle717"

# Set recursion limit so program does not end prematurely.
sys.setrecursionlimit(9999999)

def main():
    '''Main Menu'''
    print("\n{0} {1}, Copyright 2013 {2}\n".format(app, version, creator))
    print("\nPlease enter the time you want the computer to shutdown.")
    print("\nUse 24-hour format, with the following layout: 'HH:MM'")

    # So the program can loop
    global offtime

    offtime = input("\n\n> ")
    Shutdown(offtime)

# To be used later. :)
##    time.sleep(50)
##    raise SystemExit
##sys.stdout.write("Shutdown started")
##time.sleep(offtime)
##sys.stdout.write("os.system('shutdown /r /t 0')")
##sys.stdout.write("Shutting down PC...")
##os.system("shutdown /r /t 0")


def Shutdown(offtime):
    '''Checks if it is time to shutdown, and does so when ready'''


    # The current time, as defined by the System Clock
    cur_time = strftime("%H:%M", localtime())
    print(cur_time)
    print(offtime)

    # Keeps the program running until it is time.
    while True:
        if offtime == cur_time:
            print("Shutdown now!")
            sleep(1)
            raise SystemExit
        else:
            # Display "not time yet" message every 1 minute
            sleep(60)
            print("Shutdown later")
            Shutdown(offtime)

#########
## TODO:
########

# Write text file with time input
# Detect file upon startup
# If file detected: If no input in 30 seconds after startup, use time in file
# If file not detected: ask for input, proceed when given


# -- Resource links just for me. ;) -- #

#http://www.dreamincode.net/forums/topic/210175-shutting-down-a-computer-from-python/
#http://www.computerperformance.co.uk/windows7/windows7_shutdown_command.htm
#http://www.thewindowsclub.com/shutdown-restart-windows-8

if __name__ == "__main__":
    main()