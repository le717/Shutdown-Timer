"""
    Shutdown Timer -  Small Windows Shutdown Timer
    Created 2013 Triangle717 <http://triangle717.wordpress.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys, os, time
import  platform, webbrowser
import argparse, linecache
from threading import Timer

app = "Shutdown Timer"
majver = "1.0.1"
creator = "Triangle717"

# Expand recursion limit so program does not end prematurely.
sys.setrecursionlimit(999999999)

# ------------ Begin Shutdown Timer Initialization ------------ #

def CMDParse():
    '''Parses Command=line Arguments'''
    parser = argparse.ArgumentParser(description="{0} {1} Command-line arguments".format(app, majver))
    # Command-line mode argument
    parser.add_argument("-cmd", "--command",
    help="Runs {0} in command-line mode, which uses the shutdown time from ShutdownTime.txt".format(app),
    action="store_true")
    # Force shutdown argument
    parser.add_argument("-f", "--force",
    help='Sends "Force shutdown command" to Windows',
    action="store_true")
    args = parser.parse_args()

    # Declare force parameter (-f, --force) as global for use in Shutdown(offtime)
    global force, command
    force = args.force
    command = args.command

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

    # If you are running Python 3.3.0
    else:
        # You are not running Windows
        if platform.system() != 'Windows':
            print("\n{0} {1} is not supported on a non-Windows Operating System!".format(app, majver))
            print("\n{0} is shutting down.".format(app))
            time.sleep(2)
            raise SystemExit

        # You are running Windows
        else:
            # Run Command-line arguments parser
            CMDParse()
            # It was not run with the -cmd (or --command) argument
            if not command:
                main()

            # It was run with the command-line argument
            else:

                # ShutdownTime.txt does not exist
                if not os.path.exists("ShutdownTime.txt"):

                    # Go to main(), where it will be written
                    main()

                # ShutdownTime.txt does exist
                elif os.path.exists("ShutdownTime.txt"):
                    # Go to CmdMenu(), where it will be sued
                    CmdMain()

def CmdMain():
    '''Shutdown Timer Command Line Mode Menu'''

    # Write window title for command-line mode
    os.system("title {0} {1} - Command Line Mode".format(app, majver))

    print("\n{0} Version {1}, Created 2013 {2}".format(app, majver, creator))
    print('''Command Line Mode
        \nShutdownTime.txt has been detected.
Your computer will shutdown at the time written in the file.
        \nThe Shutdown sequence will begin in 10 seconds.
Pressing 'q' right now will cancel the timer.'''.format(app))

    # Start 10 second countdown timer
    # After 10 seconds, runs readFile() to get the shutdown time
    t = Timer(10.0,getTime)
    t.start()
    menuopt = input("\n\n")

    # User wanted to close the timer
    if menuopt.lower() == "q":
        t.cancel()
        print("\n{0} is shutting down.".format(app))
        time.sleep(2)
        raise SystemExit

def main():
    '''Shutdown Timer Menu Layout'''

    # Write window title for non-command-line mode
    os.system("title {0} {1}".format(app, majver))

    print("\n{0} Version {1}, Created 2013 {2}".format(app, majver, creator))
    print('''\nPlease enter the time you want the computer to shutdown.
Use the 24-hour format with the following layout: "HH:MM".
\nPress "q" to exit.''')

    offtime = input("\n\n> ")

    # Only 'q' will close the program
    if offtime.lower() == "q":
        print("\n{0} is shutting down.".format(app))
        time.sleep(2)
        raise SystemExit

    elif len(offtime) == 0:
        print("\nYou have entered an invalid time!")
        time.sleep(1.5)
        main()

    # User typed a vaild time
    else:
        # Write time to be used by CMD mode
        with open("ShutdownTime.txt", 'wt', encoding="utf-8") as file:
            print("// Shutdown Timer, copyright 2013 Triangle717", file=file)
            # Kill new line ending
            print("{0}".format(offtime), file=file, end="")

        # Now run shutdown sequence
        Shutdown(offtime)

def getTime():
    '''Reads ShutdownTime.txt for shutdown time for Command Line Mode'''

    # Read line 2 from ShutdownTime.txt for shutdown time
    offtime = linecache.getline("ShutdownTime.txt", 2)
    offtime = offtime.strip("\n")

    print("Your computer will shutdown at {0}.".format(offtime))

    # Run Shutdown sequence
    Shutdown(offtime)

def Shutdown(offtime):
    '''Checks if it is time to shutdown, and does so when ready'''

    # The current time, as defined by the System Clock
    cur_time = time.strftime("%H:%M", time.localtime())

    # Keeps the program running until it is time.
    while True:

        # The defined time equals the current (system) time
        if offtime == cur_time:
            print("\nYour computer is shutting down.")
            # Let user read message
            time.sleep(1)

            # Call hidden shutdown.exe CMD app to shutdown Windows
            # Using /p shutdowns Windows immeadity without warning,
            # Equal to using /s /t 0
            # If the force parmeter was not used
            if not force:
                os.system("shutdown.exe /p")

            # The force parmeter was used
            elif force:
                os.system("shutdown.exe /p /f ")

        # The defined time does not equal the current (system) time.
        elif offtime != cur_time:
            # Get the current seconds, as defined by the system clock.
            cur_seconds = time.strftime("%S", time.localtime())

            '''The following code aligns the timer exactly with the system clock,
            allowing the computer to begin the shutdown routine exactly when stated.'''

            if cur_seconds != 00:
                # Get how many seconds before it is aligned
                # 61 seconds because of the 1 second delay to display message
                # Conver to int(eger) to subtract
                aligntime = 61 - int(cur_seconds)

                print("\nIt is not {0}. Your computer will not shutdown.".format(offtime))
                # Sleep for however long until alignment
                time.sleep(aligntime)
                # Loop back through the program
                Shutdown(offtime)


def TODO():
    ''':P'''
    # Keeps Python from throwing some error in case somebody wants to run this. :P
    webbrowser.open_new_tab("http://triangle717.files.wordpress.com/2013/03/fabulandcow.jpg")
    os._exit(0)

# Check if input matches required format???
# Once timer is started, press 'q' to close, or Windows' exit button???
# Restart (-r, --restart_ command-line parameter (requires redo of Shutdown(offtime))
# Anything else I remember later on

if __name__ == "__main__":
    # Run program
    preload()