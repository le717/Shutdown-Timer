#! python3
# -*- coding: utf-8 -*-
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
    along with Shutdown Timer. If not, see <http://www.gnu.org/licenses/>.
"""

# Imports
import sys
import os
import time
import platform
import webbrowser
import argparse
import linecache
from threading import Timer

# Global variables
app = "Shutdown Timer"
majver = "1.0.2"
creator = "Triangle717"
# Debug variable is set to False before release
debug = False

# You need to have at least Python 3.3.0 to run this
if sys.version_info < (3,3,0):
    sys.stdout.write("\nYou need to download Python 3.3.0 or greater to run {0} {1}.".format(app, majver))
    # Don't open browser immediately
    time.sleep(2)
    webbrowser.open_new_tab("http://python.org/download") # New tab, raise browser window (if possible)
    # Close program
    time.sleep(3)
    raise SystemExit

# If you are running Python 3.3.0+
else:
    # You are not running Windows
    if platform.system() != 'Windows':
        print("\n{0} {1} is not supported on a non-Windows Operating System!".format(app, majver))
        time.sleep(2)
        raise SystemExit

# ------------ Begin Shutdown Timer Initialization ------------ #

def CMDParse():
    """Parses Command-line Arguments"""
    parser = argparse.ArgumentParser(description="{0} {1} Command-line arguments".format(app, majver))
    # Automatic  mode argument
    parser.add_argument("-a", "--auto",
    help="Runs {0} in automatic mode, using the time written in TheTime.txt".format(app),
    action="store_true")

    # Force shutdown argument
    parser.add_argument("-f", "--force",
    help='Sends "Force" command to Windows',
    action="store_true")

    # Restart Computer argument
    parser.add_argument("-r", "--restart",
    help='Restart Windows instead of shutting it down',
    action="store_true")
    args = parser.parse_args()

    # Declare force parameter (-f, --force) as global for use in Shutdown(offtime)
    global force, auto, restart
    force = args.force
    auto = args.auto
    restart = args.restart

def preload():
    """Run the correct mode, depending on parameters passed"""

    # The program was not run with the -a (or --auto) argument
    if not auto:
        main()
    # It was run with the automatic argument
    else:
        has_file = timer_File()
        # The CMD time files does not exist
        if not has_file:
            # Go to main(), where it will be written
            main()
        # The Auto time file(s) does exist
        elif has_file:
            # Go to AutoMain(), where it will be used
            AutoMain()

def timer_File():
    """Check for the existance and the usage of new or old time file"""

    global the_file
    # Both files exist, new file has priority
    if os.path.exists("ShutdownTime.txt") and os.path.exists("TheTime.txt"):
        if debug:
            print("DEBUG: Both ShutdownTime.txt and TheTime.txt exists. TheTime.txt will be used.")
        the_file = "TheTime.txt"
        return True

    # Only the old file exists
    elif os.path.exists("ShutdownTime.txt") and not os.path.exists("TheTime.txt"):
        if debug:
            print("DEBUG: ShutdownTime.txt exists, but TheTime.txt does not. ShutdownTime.txt will be used.")
        the_file = "ShutdownTime.txt"
        return True

    # Neither of the files exist
    elif not os.path.exists("ShutdownTime.txt") and not os.path.exists("TheTime.txt"):
        if debug:
            print("DEBUG: Neither ShutdownTime.txt nor TheTime.txt exists.")
        return False

    # Anything else (not really needed, but here for safety)
    else:
        if debug:
            print("DEBUG: TheTime.txt will be used.")
        the_file = "TheTime.txt"
        return True

def close_Type():
    """Change app messages depending if we are shutting down or restarting"""

    global the_word, the_word_ing
    if restart:
        if debug:
            print("DEBUG: The words are 'restart' and 'restarting'.")
        the_word = "restart"
        the_word_ing = "restarting"
    elif not restart:
        if debug:
            print("DEBUG: The words are 'shutdown' and 'shutting down'.")
        the_word = "shutdown"
        the_word_ing = "shutting down"

# ------------ End Shutdown Timer Initialization ------------ #


# ------------ Begin Shutdown Timer Menus ------------ #

def AutoMain():
    """Shutdown Timer Automatic Mode Menu"""

    # Write window title for automatic mode
    os.system("title {0} {1} - Automatic Mode".format(app, majver))

    print("\n{0} Version {1} - Automatic Mode".format(app, majver))
    print('''Created 2013 {0}

{1} has been detected.
Your computer will {2} at the time written in the file.
\nThe Timer will begin in 10 seconds.
Pressing 'q' right now will cancel the {2}.'''.format(creator, the_file, the_word))

    # Start 10 second countdown timer
    # After 10 seconds, run readFile() to get the shutdown time
    t = Timer(10.0, getTime)
    t.start()
    menuopt = input("\n\n> ")

    # User wanted to close the timer
    if menuopt.lower() == "q":
        t.cancel()
        raise SystemExit

def main():
    """Shutdown Timer Menu Layout"""

    # Write window title for non-automatic mode
    os.system("title {0} {1}".format(app, majver))

    print("\n{0} Version {1}\nCreated 2013 {2}".format(app, majver, creator))
    print('''\nPlease enter the time you want the computer to {0}.
Use the 24-hour format with the following layout: "HH:MM".
\nPress "q" to exit.'''.format(the_word))

    off_time = input("\n\n> ")

    # Only 'q' will close the program
    if off_time.lower() == "q":
        raise SystemExit

    elif len(off_time) == 0:
        print("\nYou have entered an invalid time!")
        time.sleep(1.5)
        main()

    # User typed a vaild time
    else:
        # Write time to be used by Automatic mode
        # TheTime.txt is the only file written from now on
        with open("TheTime.txt", 'wt', encoding="utf-8") as f:
            print("// Shutdown Timer, created 2013 Triangle717", file=f)
            print("{0}".format(off_time), file=f, end="")

        # Now run shutdown sequence
        theTimer(off_time)

# ------------ End Shutdown Timer Menus ------------ #


# ------------ Begin Various Timer Actions ------------ #

def getTime():
    """Reads TheTime.txt/ShutdownTime.txt for shutdown time for Automatic Mode"""

    # Read line 2 from the_file for shutdown time
    off_time = linecache.getline(the_file, 2)
    off_time = off_time.strip("\n")

    print("Your computer will {0} at {1}.".format(the_word, off_time))

    # Run timer
    theTimer(off_time)


def theTimer(off_time):
    """Gets current time and performs the appropriate actions"""

    # If the shutdown time does not equal
    # the current time, as defined by the System Clock
    while off_time != time.strftime("%H:%M", time.localtime()):
        # Required so the current time will be updated when
        # time.sleep(align_time) is finished. The line above
        # will not do this.
        cur_time = time.strftime("%H:%M", time.localtime())

        if debug:
            print("DEBUG: The current time is " + cur_time)

        # Get the current seconds, as defined by the system clock.
        cur_seconds = time.strftime("%S", time.localtime())

        if cur_seconds != 00:
            # Align the timer exactly with the system clock,
            # allowing the computer to begin the shutdown routine exactly when stated.

            # !!WARNING!!
            # Do not change align_time to anything less than 60.
            # Anything less creates a huge bug and throws the timer
            # off by a minute, or creates a negative time

            # Convert to int(eger) so we can subtract
            align_time = 60 - int(cur_seconds)

            if debug:
                print("DEBUG: Align time is " + str(align_time))

        print("\nIt is not {0}, it is only {1}. Your computer will not {2}.".format(off_time, str(cur_time), the_word))
        # Sleep for however long until alignment
        time.sleep(align_time)

    print("\nYour computer is {0}.".format(the_word_ing))
    # Let user read message
    time.sleep(1)
    close_Win()

# ------------ End Various Timer Actions ------------ #


# ------------ Begin Shutdown/Restart Commands ------------ #

def close_Win():
    """Shutsdown or Retarts Computer depending on Arguments"""

    # Call hidden shutdown.exe CMD app to shutdown/restart Windows

    # The restart command was sent
    if restart:
        # The force command was sent as well
        if force:
            if debug:
                print("DEBUG: The shutdown commmand is " + r'os.system("shutdown.exe /r /f")')
            os.system("shutdown.exe /r /f /t 0")
        # Only the restart command was sent
        elif not force:
            if debug:
                 print("DEBUG: The shutdown commmand is " + r'os.system("shutdown.exe /r /t 0")')
            os.system("shutdown.exe /r /t 0")

    # Normal shutdown commmand was sent
    elif not restart:
        # The force command was sent as well
        # Using /p shutdowns Windows immediately without warning,
        # Same as /s /t 0
        if force:
            if debug:
                print("DEBUG: The shutdown commmand is " + r'os.system("shutdown.exe /p /f")')
            os.system("shutdown.exe /p /f")
        # The force command was not sent
        elif not force:
            if debug:
                print("DEBUG: The shutdown commmand is " + r'os.system("shutdown.exe /p")')
            os.system("shutdown.exe /p")

# ------------ End Shutdown/Restart Commands ------------ #

"""TODO List"""

# OS X or Linux commands for cross-platform support?
# Check if input matches required format???
# Once timer is started, press 'q' to close, or window exit button???
# Anything else I remember later on

if __name__ == "__main__":
    # Run program
    CMDParse()
    close_Type()
    preload()