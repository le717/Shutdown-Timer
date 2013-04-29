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

# Expand recursion limit so program does not end prematurely.
# TODO: Might be faulty, see TODO() comments 1-2
sys.setrecursionlimit(999999999)

# ------------ Begin Shutdown Timer Initialization ------------ #

def CMDParse():
    '''Parses Command=line Arguments'''
    parser = argparse.ArgumentParser(description="{0} {1} Command-line arguments".format(app, majver))
    # Command-line mode argument
    parser.add_argument("-cmd", "--command",
    help="Runs {0} in command-line mode, using the shutdown time in TheTime.txt".format(app),
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
    global force, command, restart
    force = args.force
    command = args.command
    restart = args.restart

def preload():
    '''Python 3.3.0 & ShutdownTime.txt check'''

    # You need to have at least Python 3.3.0 to run this
    if sys.version_info < (3,3,0):
        sys.stdout.write("\nYou need to download Python 3.3.0 or greater to run {0} {1}.".format(app, majver))
        # Don't open browser immediately
        time.sleep(2)
        webbrowser.open_new_tab("http://python.org/download") # New tab, raise browser window (if possible)
        # Close app
        time.sleep(3)
        raise SystemExit

    # If you are running Python 3.3.0+
    else:
        # You are not running Windows
        if platform.system() != 'Windows':
            print("\n{0} {1} is not supported on a non-Windows Operating System!".format(app, majver))
            print("\n{0} is shutting down.".format(app))
            time.sleep(2)
            raise SystemExit

        # You are running Windows
        else:
            close_Type()
            # It was not run with the -cmd (or --command) argument
            if not command:
                main()
            # It was run with the command-line argument
            else:
                has_file = timer_File()
                # The CMD time files does not exist
                if has_file == False:
                    # Go to main(), where it will be written
                    main()
                # The CMD time files does exist
                elif has_file == True:
                    # Go to CmdMenu(), where it will be used
                    CmdMain()

def timer_File():
    '''Check for the existance and the usagev of new or old CMD time file'''

    global the_file
    # Both files exist, new file has priority
    if os.path.exists("ShutdownTime.txt") and os.path.exists("TheTime.txt"):
        the_file = "TheTime.txt"
        return True
    # Only the old file exists
    elif os.path.exists("ShutdownTime.txt") and not os.path.exists("TheTime.txt"):
        the_file = "ShutdownTime.txt"
        return True
    # Neither of the files exist
    elif not os.path.exists("ShutdownTime.txt") and not os.path.exists("TheTime.txt"):
        return False
    # Anything else (not really needed, but here for safety)
    else:
        the_file = "TheTime.txt"
        return True

def close_Type():
    '''Change app messages depending if we are shutting down or restarting'''

    global the_word, the_word_ing
    if restart:
        the_word = "restart"
        the_word_ing = "restarting"
    elif not restart:
        the_word = "shutdown"
        the_word_ing = "shutting down"

# ------------ End Shutdown Timer Initialization ------------ #


# ------------ Begin Shutdown Timer Menus ------------ #

def CmdMain():
    '''Shutdown Timer Command Line Mode Menu'''

    # Write window title for command-line mode
    os.system("title {0} {1} - Command Line Mode".format(app, majver))

    print("\n{0} Version {1}, Created 2013 {2}".format(app, majver, creator))
    print('''Command Line Mode
{0} has been detected.
Your computer will {1} at the time written in the file.
\nThe Timer will begin in 10 seconds.
Pressing 'q' right now will cancel the {1}.'''.format(the_file, the_word))

    # Start 10 second countdown timer
    # After 10 seconds, run readFile() to get the shutdown time
    t = Timer(10.0, getTime)
    t.start()
    menuopt = input("\n\n")

    # User wanted to close the timer
    if menuopt.lower() == "q":
        t.cancel()
        # print("\n{0} is shutting down.".format(app))
        # time.sleep(2)
        raise SystemExit

def main():
    '''Shutdown Timer Menu Layout'''

    # Write window title for non-command-line mode
    os.system("title {0} {1}".format(app, majver))

    print("\n{0} Version {1}, Created 2013 {2}".format(app, majver, creator))
    print('''\nPlease enter the time you want the computer to {0}.
Use the 24-hour format with the following layout: "HH:MM".
\nPress "q" to exit.'''.format(the_word))

    off_time = input("\n\n> ")

    # Only 'q' will close the program
    if off_time.lower() == "q":
        # print("\n{0} is shutting down.".format(app))
        # time.sleep(2)
        raise SystemExit

    elif len(off_time) == 0:
        print("\nYou have entered an invalid time!")
        time.sleep(1.5)
        main()

    # User typed a vaild time
    else:
        # Write time to be used by CMD mode
        # TheTime.txt is the only file written from now on
        with open("TheTime.txt", 'wt', encoding="utf-8") as f:
            print("// Shutdown Timer, created 2013 Triangle717", file=f)
            print("{0}".format(off_time), file=f, end="")

        # Now run shutdown sequence
        TheTimer(off_time)

# ------------ End Shutdown Timer Menus ------------ #


# ------------ Begin Various Timer Actions ------------ #

def getTime():
    '''Reads TheTime.txt/ShutdownTime.txt for shutdown time for Command Line Mode'''

    # Read line 2 from the_file for shutdown time
    off_time = linecache.getline(the_file, 2)
    off_time = off_time.strip("\n")

    print("Your computer will {0} at {1}.".format(the_word, off_time))

    # Run timer
    TheTimer(off_time)

def TheTimer(off_time):
    '''Gets current time and performs the appropriate actions
    Note: This is still WIP, as all the bugs have not been ironed out'''

    # The current time, as defined by the System Clock
    cur_time = time.strftime("%H:%M", time.localtime())

    if off_time != cur_time:
        while off_time != cur_time:
            # Get the current seconds, as defined by the system clock.
            cur_seconds = time.strftime("%S", time.localtime())

            '''The following code aligns the timer exactly with the system clock,
            allowing the computer to begin the shutdown routine exactly when stated.'''

            if cur_seconds != 00:
                # Get how many seconds before it is aligned
                # 61 seconds because of the 1 second delay to display message
                # Conver to int(eger) to subtract
                aligntime = 61 - int(cur_seconds)

                print("\nIt is not {0}. Your computer will not {1}.".format(off_time, the_word))
                # Sleep for however long until alignment
                time.sleep(aligntime)
                TheTimer(off_time)

    elif off_time == cur_time:
        print("\nYour computer is {0}.".format(the_word_ing))
        # Let user read message
        time.sleep(1)
        close_Win()

# ------------ End Various Timer Actions ------------ #


# ------------ Begin Actual Shutdown/Restart Action ------------ #

def close_Win():
    '''Shutsdown or Retarts Computer depending on Arguments'''

    # Call hidden shutdown.exe CMD app to shutdown/restart Windows

    # The restart command was sent
    if restart:
        # The force command was sent as well
        if force:
            os.system("shutdown.exe /r /f")
        elif not force:
            os.system("shutdown.exe /r")

    # Normal shutdown commmand was sent
    elif not restart:
        # The force command was sent as well
        # Using /p shutdowns Windows immediately without warning,
        # Same as /s /t 0
        if force:
            os.system("shutdown.exe /p /f")
        # The force command was not sent
        elif not force:
            os.system("shutdown.exe /p")

# ------------ End Actual Shutdown/Restart Action ------------ #

def TODO():
    ''':P'''
    # Keeps Python from throwing some error in case somebody wants to run this. :P
    webbrowser.open_new_tab("http://triangle717.files.wordpress.com/2013/03/fabulandcow.jpg")
    os._exit(0)

# Rework the looping method to make this work if Windows is booted in early morning
# Look at the PatchIt! Uninstaller for help
# Check if input matches required format???
# Once timer is started, press 'q' to close, or Windows' exit button???
# Anything else I remember later on

if __name__ == "__main__":
    # Run program
    CMDParse()
    preload()
